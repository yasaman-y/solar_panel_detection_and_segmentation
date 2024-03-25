// this is the example code for download polygon as geojson file for later download correspond image
// this code is in java script for run in google earth engin code editor


// Replace with your polygon coordinates
var polygon = ee.Geometry.Polygon(geometry_limon);

// var polygon = ee.Geometry.Polygon([
//   [-122.090, 37.424],
//   [-122.084, 37.424],
//   [-122.084, 37.431],
//   [-122.090, 37.431]
// ]);

Export.table.toDrive({
  collection: ee.FeatureCollection(geometry_limon),
  description: 'geometry_limon',
  fileFormat: 'GeoJSON',
  folder : "geojason"
});
