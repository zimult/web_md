var DOMAIN = "http://emoji.biaoqingmm.com:4567";
var uid = localStorage.getItem("uid");
var token = localStorage.getItem("token");
// var DOMAIN = "http://localhost:4567";

var _submit = function(url, type, params, callback) {
    var method = type;
    if (type == null || type.length == 0) {
        method = "GET";
    };
    params = params ? Object.assign(params,  {"uid": uid}, {"token": token}) : {}
    $.ajax({
        type: method,
        data: params,
        url: url,
        success: function(data) {
            var code = data.code
            if (code == 1) {
                callback(params, data, null);
            }else {
                var message = data.error;
                if (message.indexOf("未登录") > -1) {
                  callback(params, null, "errorCode" + code + " " + message + " , 即将跳转到登录页面");
                  window.location.href = '../image-tools/user-login.html';
                } else {
                  callback(params, null, "errorCode" + code + " " + message);
                }
            }
        },
        error: function(error) {
            callback(params, null, "errorCode" + error.status + " " + error.statusText);
        },
        dataType: "json"
    });
}


var _genSignature = function(url, params) {
    var names = [];
    for(var n in params){
        names.push(n);
    }

    var paramString = url
    names.sort();
    for (var nameIndex in names) {
        var key = names[nameIndex];
        var value = params[key];
        paramString += nameIndex == 0 ? '' : '&';
        paramString += key + '=' + value;
    }
    return md5(paramString).toUpperCase();
}

//上传文件
var _submit3 = function(url, type, params, callback) {
    var method = type;
    if (type == null || type.length == 0) {
        method = "GET";
    };
    params = params ? Object.assign(params,  {"uid": uid}, {"token": token}) : {}
    $.ajax({
        type: method,
        data: params,
        url: url,
        processData: false,
        contentType: false,
        success: function(data) {
            var code = data.code
            if (code == 1) {
                callback(params, data, null);
            }else {
                console.log("data" + data);
                var message = data.error;
                if (message.indexOf("未登录") > -1) {
                  callback(params, null, "errorCode" + code + " " + message + " , 即将跳转到登录页面");
                  window.location.href = '../image-tools/user-login.html';
                } else {
                  callback(params, null, "errorCode" + code + " " + message);
                }
            }
        },
        error: function(error) {
            console.log(error);
            callback(params, null, "errorCode" + error.status + " " + error.statusText);
        },
        dataType: "json"
    });
}

function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)","i")
    var result = window.location.search.substr(1).match(reg)
    if (result != null) {
        return result[2]
    } else {
        return null
    }
}


function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}


function colorHex2RGB(sColor) {
    var sColor = sColor.toLowerCase();
    var step = 2//六位
    if(sColor.length == 3){
        step = 1
    }
    var length = step * 3
    var rgbColor = [];
    for(var i=0; i<length; i+=step){
        rgbColor.push(parseInt("0x"+sColor.slice(i,i+step)));
    }
    return rgbColor
}
