function runMyGuy() {
  let device;
  try {
    device = navigator.usb.requestDevice({ filters: [{
        vendorId: 0x1fc9,
        productId: 0x000C
    }]});
  } catch (err) {
    // No device was selected.
  }

  if (device !== undefined) {
    // Add |device| to the UI.
  }

  console.log(device);
}