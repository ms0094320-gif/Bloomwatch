import os, glob, argparse, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
import tensorflow as tf
from tensorflow.keras import layers, models

def load_csv(path):
    df = pd.read_csv(path)
    # Expected columns: time, NDVI, EVI
    df = df.sort_values(df.columns[0])
    return df[['NDVI','EVI']].interpolate().bfill().ffill()

def make_windows(arr, w=8, stride=1):
    X = []
    for i in range(0, len(arr)-w+1, stride):
        X.append(arr[i:i+w])
    return np.array(X)

def build_lstm(input_shape):
    m = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv1D(32, 3, activation='relu'),
        layers.MaxPooling1D(2),
        layers.Bidirectional(layers.LSTM(64)),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return m

def main(args):
    files = glob.glob(os.path.join(args.data, '*.csv'))
    if not files:
        raise SystemExit(f'No CSV files found in {args.data}. Export from GEE first.')
    X_all, y_all = [], []
    for f in files:
        df = load_csv(f).values
        X = make_windows(df, w=args.window)
        # Demo labels: windows with NDVI jump > 0.05 are positive (replace with real labels)
        y = ((X[:,:,0].max(axis=1) - X[:,:,0].min(axis=1)) > 0.05).astype(int)
        X_all.append(X); y_all.append(y)
    X_all = np.vstack(X_all); y_all = np.concatenate(y_all)

    Xtr, Xva, ytr, yva = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
    lstm = build_lstm(Xtr.shape[1:])
    lstm.fit(Xtr, ytr, epochs=5, batch_size=32, validation_data=(Xva, yva))
    os.makedirs(args.out, exist_ok=True)
    lstm.save(os.path.join(args.out, 'lstm_bloomwatch.h5'))

    # XGBoost features (summary stats)
    def feats(X):
        return np.c_[X[:,:,0].mean(1), X[:,:,0].std(1), X[:,:,0].ptp(1),
                     X[:,:,1].mean(1), X[:,:,1].std(1)]
    dtr = xgb.DMatrix(feats(Xtr), label=ytr)
    dva = xgb.DMatrix(feats(Xva), label=yva)
    params = dict(max_depth=4, eta=0.2, objective='binary:logistic', eval_metric='logloss')
    bst = xgb.train(params, dtr, num_boost_round=80, evals=[(dva,'val')])
    bst.save_model(os.path.join(args.out, 'xgb_bloomwatch.json'))
    print('Models saved to', args.out)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='data/exports/')
    ap.add_argument('--out', default='models/')
    ap.add_argument('--window', type=int, default=8)
    args = ap.parse_args()
    main(args)