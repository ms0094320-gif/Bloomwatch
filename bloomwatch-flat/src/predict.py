import json, argparse, numpy as np, pandas as pd, tensorflow as tf, xgboost as xgb

def load_csv(path):
    df = pd.read_csv(path).sort_values(df.columns[0])
    return df[['NDVI','EVI']].interpolate().bfill().ffill().values

def make_windows(arr, w=8, stride=1):
    X = []
    for i in range(0, len(arr)-w+1, stride):
        X.append(arr[i:i+w])
    return np.array(X)

def feats(X):
    return np.c_[X[:,:,0].mean(1), X[:,:,0].std(1), X[:,:,0].ptp(1),
                 X[:,:,1].mean(1), X[:,:,1].std(1)]

def main(args):
    arr = load_csv(args.input)
    X = make_windows(arr, w=args.window)
    lstm = tf.keras.models.load_model('models/lstm_bloomwatch.h5')
    xgbm = xgb.Booster(); xgbm.load_model('models/xgb_bloomwatch.json')
    p_lstm = lstm.predict(X, verbose=0).ravel()
    p_xgb  = xgbm.predict(xgb.DMatrix(feats(X)))
    p = (p_lstm*0.6 + p_xgb*0.4)
    idx = int(p.argmax())
    out = dict(bloom_window_start=int(idx), confidence=float(p[idx]))
    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--out', default='results/bloom.json')
    ap.add_argument('--window', type=int, default=8)
    main(ap.parse_args())