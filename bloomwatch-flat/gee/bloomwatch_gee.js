// BloomWatch — Earth Engine starter
// Paste into https://code.earthengine.google.com/

var region = /* replace with your AOI */ ee.Geometry.Point([55.976, 23.588]).buffer(2000);
var start = '2021-01-01';
var end   = '2024-12-31';

var mod13 = ee.ImageCollection('MODIS/061/MOD13Q1')
  .filterDate(start, end)
  .select(['NDVI','EVI']);

function scaleMODIS(img){
  return img.select(['NDVI','EVI']).multiply(0.0001)
            .copyProperties(img, ['system:time_start']);
}

var ts = mod13.map(scaleMODIS).map(function(img){
  var reduced = img.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: region,
    scale: 250,
    maxPixels: 1e9
  });
  return ee.Feature(null, {
    'time': img.get('system:time_start'),
    'NDVI': reduced.get('NDVI'),
    'EVI': reduced.get('EVI')
  });
});

Export.table.toDrive({
  collection: ee.FeatureCollection(ts),
  description: 'bloomwatch_timeseries_export',
  fileFormat: 'CSV'
});