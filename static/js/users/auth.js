var $sUsername = document.getElementById("user_name");
var $sPassword = document.getElementById("pwd1");
var $sPwd = document.getElementById("pwd2");
var $sMobile = document.getElementById("mobile");
var $register = $('.form-contain');


$register.submit(function (e) {
    // 阻止默认提交操作
    e.preventDefault();

    // 获取用户输入的内容
    let sUsername = $sUsername.value;  // 获取用户输入的用户名字符串
    let sPassword = $sPassword.value;
    let sPwd = $sPwd.value;
    let sMobile = $sMobile.value;  // 获取用户输入的手机号码字符串
    let SdataParams = {
      "username": sUsername,
      "password": sPassword,
      "password_repeat": sPwd,
      "mobile": sMobile,
    };

    // 2、创建ajax请求
    $.ajax({
      // 请求地址
      url: "/users/register/",  // url尾部需要添加/
      // 请求方式
      type: "POST",
      data: JSON.stringify(SdataParams),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
        .done(function (res) {
          if (res.errno === "0") {
            // 注册成功
            alert('success');
            setTimeout(function () {
              // 注册成功之后重定向到主页
              window.location.href = document.referrer;
              // window.location.href = '/users/login/';
            }, 1000)
          } else {
            // 注册失败，打印错误信息
            alert('注册失败')
          }
        })
        .fail(function () {
          alert('服务器超时')
        });

  });
// $sUsername.blur(function () {
//   fn_check_usrname();
// });
// window.onload = function () {
//   $sUsername.onchange = checkForm();
//   $sPassword.onchange = checkForm();
//   $sPwd.onchange = checkForm()
// };
// function fn_check_usrname() {
//   let sUsername = $sUsername.value;
//   if (sUsername === "") {
//     //2.给出错误提示信息
//     // sUsername.setCustomValidity('用户名不能为空');
//     alert("用户名不能为空!");
//     return false;
//   }
// }
// function checkForm() {
//   let sUsername = $sUsername.value;
//   let sPassword = $sPassword.value;
//   let sPwd = $sPwd.value;
//   //alert("aa");
//   /**校验用户名*/
//       //1.获取用户输入的数据
//   //alert(sUsername);
//
//
//   /*校验密码*/
//   if (sPassword === "") {
//     sPassword.setCustomValidity('密码不能为空');
//     // alert("密码不能为空!");
//     return false;
//   }
//
//   /**校验确认密码*/
//   if (sPwd !== sPassword) {
//     sPwd.setCustomValidity('两次密码输入不一致!');
//     // alert("两次密码输入不一致!");
//     return false;
//   }
//
//   // /*校验邮箱*/
//   // var eValue = document.getElementById("eamil").value;
//   // if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/.test(eValue)) {
//   //   alert("邮箱格式不正确!");
//   //   return false;
//   // }
//   var sMobile = document.getElementById('mobile');
//   if (sMobile === "") {
//     sMobile.setCustomValidity('手机号不能为空！');
//     return false
//   }
//
// }
