const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('api', {
  // later, you can define secure bridges here
});
