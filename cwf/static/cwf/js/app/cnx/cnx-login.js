cwf.cnxEntryForms = (function () {
  const uiSelectors = {};
  function initCnxEntryForms() {
    uiSelectors.moduleDiv = $("body");
    uiSelectors.moduleDiv.haml(setupCnxEntryFormsUI());
    console.log(cwf.currentUser);

    setupUITriggers();
  }

  function setupCnxEntryFormsUI() {
    return [
      ["%div.container", getCnxEntryTitleUI()],
      [
        "%div.container-xl",
        [
          "%div.x-wrapper",
          { style: "height: 100%;" },
          [
            "%div.container.login-wrapper",
            { style: "margin-top: 16px;" },
            [
              "%div.x-wrapper",
              { style: "margin-top: 16px;" },
              ["%div.signing-forms", getSigningFormsUI()],
            ],
          ],
        ],
      ],
    ];
  }

  function getCnxEntryTitleUI() {
    return [
      [
        "%a",
        { href: "/" },
        [
          "%img.logo",
          {
            src: "/static/cwf/images/cnx_logo_full.svg",
            alt: "CineX Logo",
          },
        ],
      ],
    ];
  }

  function getSigningFormsUI() {
    return [
      ["%h2.clr-pri.tagline", "not", ["%span.clr-sec", " IMDB"]],
      [
        "%div.forms-main-container",
        { style: "margin-top: 16px;" },
        [
          "%input",
          { type: "radio", id: "sign-in", name: "sign-in-tabs", checked: "" },
        ],
        ["%label", { for: "sign-in" }, "Sign In"],
        ["%input", { type: "radio", id: "sign-up", name: "sign-in-tabs" }],
        ["%label", { for: "sign-up" }, "Sign Up"],
        ["%div.line"],
        ["%hr"],
        [
          "%div.forms-container",
          ["%div.forms-content", { id: "sign-in-content" }, getSignInFormUI()],
          [
            "%div.forms-content",
            { id: "sign-up-content", style: "display: none;" },
            getSignUpFormUI(),
          ],
        ],
      ],
    ];
  }

  function getSignInFormUI() {
    return [
      "%form.login.active",
      {
        id: "loginForm",
        name: "loginForm",
        // action: homePageURL,
        action: "/",
        // action: 'Login',
        method: "post",
        enctype: "multipart/form-data",
      },
      [
        "%div.x-wrapper",
        { style: "margin-top: 24px;" },
        [
          "%div.login-fields-wrapper",
          { id: "si-user-id-div" },
          ["%span.input-label", "Email*"],
          ["%input", { id: "user_id", name: "user_id", type: "text" }],
        ],
        [
          "%div.login-fields-wrapper",
          { id: "si-password-div" },
          [
            "%span.input-label",
            "Password*" /*['%img', {src: '/static/cwf/images/eye-slash.svg'}]*/,
          ],
          ["%input", { type: "password", id: "password", name: "password" }],
        ],
        [
          "%div.button",
          [
            "%button",
            { type: "submit", id: "id_login", name: "action" },
            "Sign In",
          ],
        ],
      ],
    ];
  }

  function getSignUpFormUI() {
    return [
      "%div.x-wrapper",
      [
        "%div.col-12.col-md-6",
        { id: "su-usr-name-div" },
        ["%span.input-label", "Name*"],
        ["%input.d-block.w-75.w-100", { type: "text", id: "su-usr-name" }],
      ],
      [
        "%div.col-12.col-md-6",
        { id: "su-usr-email-div" },
        ["%span.input-label", "Email*"],
        [
          "%input.d-block.w-75.w-100",
          { type: "text", id: "su-usr-email", autocomplete: "off" },
        ],
      ],
      [
        "%div.col-12.col-md-6",
        { id: "su-password-div" },
        ["%span.input-label", "Password*"],
        [
          "%input.d-block.w-75.w-100",
          { type: "password", id: "su-password", autocomplete: "off" },
        ],
      ],
      [
        "%div.col-12.col-md-6",
        { id: "su-cf-password-div" },
        ["%span.input-label", "Confirm Password*"],
        [
          "%input.d-block.w-75.w-100",
          { type: "password", id: "su-cf-password", autocomplete: "off" },
        ],
      ],
      [
        "%div.button",
        ["%button", { type: "submit", id: "id_signup" }, "Sign Up"],
      ],
    ];
  }

  function clearMsg() {
    uiSelectors.moduleDiv.find(".errors").remove();
  }

  function validateSigninForm() {
    clearMsg();
    const usrEmail = uiSelectors.moduleDiv.find("#user_id").val().trim(),
      usrPassword = uiSelectors.moduleDiv.find("#password").val().trim();
    let isValidate = true;

    if (usrEmail === "") {
      isValidate = false;
      $("#si-user-id-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter email"],
      ]);
    }

    if (usrPassword === "") {
      isValidate = false;
      $("#si-password-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter a password"],
      ]);
    }

    if (!cwf.utils.validateEmailId(usrEmail)) {
      isValidate = false;
      $("#si-user-id-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter a valid email"],
      ]);
    }

    return isValidate;
  }

  function validateSignupForm() {
    clearMsg();
    const usrName = uiSelectors.moduleDiv.find("#su-usr-name").val().trim(),
      usrEmail = uiSelectors.moduleDiv.find("#su-usr-email").val().trim(),
      usrPassword = uiSelectors.moduleDiv.find("#su-password").val().trim(),
      usrConfirmPassword = uiSelectors.moduleDiv
        .find("#su-cf-password")
        .val()
        .trim();
    let isValidate = true;

    if (usrName === "") {
      isValidate = false;
      $("#su-usr-name-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter name"],
      ]);
    }

    if (usrEmail === "") {
      isValidate = false;
      $("#su-usr-email-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter email"],
      ]);
    }

    if (usrPassword === "") {
      isValidate = false;
      $("#su-password-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter a password"],
      ]);
    }

    if (usrConfirmPassword === "") {
      isValidate = false;
      $("#su-cf-password-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please re-enter password"],
      ]);
    }

    if (!cwf.utils.validateEmailId(usrEmail)) {
      isValidate = false;
      $("#su-usr-email-div").haml([
        ["%div.errors", { style: "color: red;" }, "Please enter a valid email"],
      ]);
    }

    if (usrPassword !== usrConfirmPassword) {
      isValidate = false;
      $("#su-cf-password-div").haml([
        ["%div.errors", { style: "color: red;" }, "Passwords are not matching"],
      ]);
    }

    return isValidate;
  }

  function submitSignupDetails() {
    const usrSignUpObj = {
      usr_name: uiSelectors.moduleDiv.find("#su-usr-name").val().trim(),
      usr_email: uiSelectors.moduleDiv.find("#su-usr-email").val().trim(),
      usr_pswd: uiSelectors.moduleDiv.find("#su-password").val().trim(),
    };
    $.ajax({
      url: "/onboard-user/",
      type: "POST",
      data: JSON.stringify(usrSignUpObj),
      success: function (response) {
        console.log("signup response", response);
      },
      error: function (error) {
        alert("error: ", error);
      },
    });
  }

  function setupUITriggers() {
    uiSelectors.moduleDiv.on("change", "#sign-in", function () {
      $("#sign-up-content").hide();
      $("#sign-in-content").show();
    });

    uiSelectors.moduleDiv.on("change", "#sign-up", function () {
      $("#sign-in-content").hide();
      $("#sign-up-content").show();
    });

    uiSelectors.moduleDiv.on("click", "#id_login", function () {
      if (!validateSigninForm()) {
        return false;
      }
    });

    uiSelectors.moduleDiv.on("click", "#id_signup", function () {
      if (!validateSignupForm()) {
        return false;
      }
      submitSignupDetails();
    });
  }

  return {
    initCnxEntryForms: initCnxEntryForms,
  };
})();
