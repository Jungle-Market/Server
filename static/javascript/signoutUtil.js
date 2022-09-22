function onLogout() {
    $.ajax({
      type: "get",
      url:"/signout",
      success: function (res) {
        if (res.login == false) {
          location.href="/signin";
        }
      },
    });
  }