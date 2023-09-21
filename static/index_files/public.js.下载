Vue.config.devtools = "development";
var MyPlugin = {};

/**
 * 错误码处理定义
 */

MyPlugin["filters"] = {
    //异常
    "9999" : function(result) {
        layer.msg(result.msg, {icon: 0,time:2000});
    },
    //配置统一未登录错误码处理
    "-1" : function(result) {
        //未登录，跳转登陆页
        top.window.location.href = fsConfig["global"]["loginUrl"];
    }
};

/**
 * 项目中需要调用到的常量、变量这里配置
 */
MyPlugin["global"] = {
    "servletUrl":"", //使用网关请求地址,本地工程可以不填
    "port":18201,
    "token": sessionStorage.getItem("token"),//后台的token 
    "appId": sessionStorage.getItem("appId"),
    "result" : { //响应结果配置
        "statusName": "code", //数据状态的字段名称，默认：errorNo
        "msgName": "msg", //状态信息的字段名称，默认：errorInfo
        "successNo" : "0000", //执行成功错误码统一配置
        "dataName" : "data" //非表格数据的字段名称，默认：results.data
    },
    "page" : { //分页配置
        "request": {//请求配置
            "pageName": "current", //页码的参数名称，默认：pageNum
            "limitName": "size" //每页数据量的参数名，默认：pageSize
        },
        "response": {//响应配置
            "countName": "data.total", //数据总数的字段名称，默认：results.data.total
            "dataNamePage": "data.records" //分页数据列表的字段名称，默认：results.data.list
        },
        "limit":10,//每页分页数量。默认20
        "limits":[10,20,30,50,100]//每页数据选择项，默认[10,20,30,50,100]
    }
};


MyPlugin.install = function (Vue, options) {
    // 1. 添加全局方法或属性
    Vue.myGlobalMethod = function () {
      // 逻辑...
    }
  
    //非空判断
    Vue.isEmpty=function(value) {
        if (value === null || value == undefined || value === '') {
            return true;
        }
        return false;
    }
    //获取对象指
    Vue.result=function(object, path, defaultValue) {
        var value = "";
        if(!$.isEmpty(object) && $.isObject(object) && !Vue.isEmpty(path)){
            var paths = path.split('.');
            var length = paths.length;
            $.each(paths,function(i,v){
                object = object[v];
                if(length-1 == i){
                    value = object;
                }
                if(!$.isObject(object)){
                    return false;
                }
            })

        }

        if(Vue.isEmpty(value) && !Vue.isEmpty(defaultValue)){
            value = defaultValue;
        }
        return value;
    }
    Vue.getQueryString= function (name) {
        var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        var r = window.location.search.substr(1).match(reg);
        if (r != null) {
            return unescape(r[2]);
        }
        return null;
    }
    Vue.formatDate=function(date,fmt){
        if(arguments.length<2){
            fmt = "yyyy-MM-dd HH:mm:ss";
        }
        var _this = date;
        var o = {
            "M+" : _this.getMonth()+1, //月份
            "d+" : _this.getDate(), //日
            "h+" : _this.getHours()%12 == 0 ? 12 : _this.getHours()%12, //小时
            "H+" : _this.getHours(), //小时
            "m+" : _this.getMinutes(), //分
            "s+" : _this.getSeconds(), //秒
            "q+" : Math.floor((_this.getMonth()+3)/3), //季度
            "S" : _this.getMilliseconds() //毫秒
        };
        if(/(y+)/.test(fmt)){
            fmt=fmt.replace(RegExp.$1, (_this.getFullYear()+"").substr(4 - RegExp.$1.length));
        }
        for(var k in o){
            if(new RegExp("("+ k +")").test(fmt)){
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
            }
        }
        return fmt;
    }
    // 2. 添加全局资源
    Vue.directive('my-directive', {
      // bind (el, binding, vnode, oldVnode) {
        // 逻辑...
      // }
    })
  
    // 3. 注入组件
    Vue.mixin({
      created: function () {
        // 逻辑...
      }
    })
    Vue.prototype.getQueryString = Vue.getQueryString;
    Vue.prototype.formatDate = Vue.formatDate;
    // 4. 添加事例方法
    Vue.prototype.invoke = function(url,param,callBackFunc,method,async){
      // 逻辑...
		if(!Vue.isEmpty(url)){
			url = Vue.result(MyPlugin,"global.servletUrl")+ url;
		}
		if(Vue.isEmpty(async)){
			async = true;
		}
		if(Vue.isEmpty(method)){
			method = "post";
		}
		var token = Vue.result(aliConfig,"global.token");
		var appId = Vue.result(aliConfig,"global.appId");
		$.ajaxSetup({
			beforeSend:function(request, settings) {
				if (token) {
					request.setRequestHeader("Authorization", token);
				}
				if (appId) {
					request.setRequestHeader("appId", appId);
				}
			}
		});
        $.ajax({
            url: url,
            type: method,
            async: async,
            timeout: 10000,
            data: param,
            dataType : "json",
            // contentType:'application/json;charset=utf-8',
            success: function(result){
            if(result[statusName] != successNo){
                var filters = MyPlugin["filters"];
                if(!Vue.isEmpty(filters)){
                var otherFunction = filters[result[statusName]];
                if($.isFunction(otherFunction)){
                    otherFunction(result);
                    return;
                }
                }
            }
            callBackFunc(result);
            },
            error : function (XMLHttpRequest, textStatus, errorThrown)
            {
                var status = XMLHttpRequest.status;
                if(status==404){
                    fsCommon.errorMsg("请求地址出错!");
            }else if(status==302){
                fsCommon.errorMsg('连接网页出错!');
            }else if(textStatus=="timeout"){
                fsCommon.errorMsg("请求超时!");
            }else{
                fsCommon.errorMsg('请求异常!');
            }
            },
            complete : function(XMLHttpRequest, textStatus)
            {
                //关闭加载层
            }
        });
    };
  }

// 调用 `MyPlugin.install(Vue)`
Vue.use(MyPlugin);


// var appOwner = ${owner};
// var token =gettoken(${mode});
var owner = "1581564523";
var token ="preview";
$.ajaxSetup({
beforeSend:function(request, settings) {
    request.setRequestHeader("Authorization", token);
    request.setRequestHeader("owner", owner);
}
});


