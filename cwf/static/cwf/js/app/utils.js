(function ($) {
  $.extend({
    splitAttrString: function (theStr) {
      var attrs = [];
      var RefString = function (s) {
        this.value = s;
      };
      RefString.prototype.toString = function () {
        return this.value;
      };
      RefString.prototype.charAt = String.prototype.charAt;
      var data = new RefString(theStr);
      var getBlock = function (endChr, restString) {
        var block = "";
        var currChr = "";
        while (currChr != endChr && restString.value !== "") {
          if (/'|"/.test(currChr)) {
            block = block.trim() + getBlock(currChr, restString);
          } else {
            block += currChr;
          }
          currChr = restString.charAt(0);
          restString.value = restString.value.slice(1);
        }
        return block.trim();
      };

      do {
        var attr = getBlock(",", data);
        attrs.push(attr);
      } while (data.value !== "");
      return attrs;
    },
  });
})(jQuery);

cwf.utils = {
  validateEmailId: function (emailID) {
    var emailRegex =
      /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!emailRegex.test(emailID)) {
      return false;
    }
    return true;
  },
};
