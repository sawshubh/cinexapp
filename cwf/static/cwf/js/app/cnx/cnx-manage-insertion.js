cwf.cnxInsertion = (function () {
  const uiSelectors = {};
  function manageInsertionUI() {
    uiSelectors.moduleDiv = $("body");
    uiSelectors.moduleDiv.haml(setupCnxInsertionUI());

    setupUITriggers();
  }

  function setupCnxInsertionUI() {
    return [
      "%div.insertion-container-div",
      getCnxFileUploadUI(),
      getCnxInsertBtnUI(),
    ];
  }

  function getCnxFileUploadUI() {
    return [
      "%div.file-upload-div",
      ["%input", { type: "file", id: "csv-file-upload" }],
      ["%label", { for: "csv-file-upload" }, "Upload Movie CSV"],
    ];
  }

  function getCnxInsertBtnUI() {
    return [
      "%div.insert-csv-div",
      ["%button", { type: "submit", id: "insert-btn" }, "Insert Movie CSV"],
    ];
  }

  return { manageInsertionUI: manageInsertionUI };

  function setupUITriggers() {}
})();
