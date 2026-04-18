/* Main entry — loads slide modules in order and writes the pptx. */
const lib = require('./build_logistics_pitch.js');
require('./slides_01_10.js');
require('./slides_11_20.js');
require('./slides_21_30.js');
require('./slides_31_40.js');

lib.pres.writeFile({ fileName: lib.OUT }).then(name => {
  console.log('WROTE: ' + name);
}).catch(err => {
  console.error('ERROR: ', err);
  process.exit(1);
});
