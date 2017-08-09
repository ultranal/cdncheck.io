// todo: 前端路由

$.ajaxSetup({
 contentType:"application/json; charset=utf-8"
});

var app_ip = new Vue({
    el: '#ip',
    data: {
        hostname: "",
        iprange: "",
        spec: "",
        onlySuccFlag: true,
        ansList:  []
    },
    methods: {
        doIpLookup: function() {
            // todo: 异步请求、异步返回
            // todo: IPrange转化成实际ip 放在 ViewModel or Model?
            // [*] 目前版本放在Model端执行（是Model原有的功能）
            // this.ansList.push({
            //     ip: "192.168.0.1",
            //     status: "连接超时",
            //     retClass: "warning"
            // })
            this.ansList = [];
            req = {
                'hostname': this.hostname,
                'iprange': this.iprange,
                'spec': this.spec,
                'onlySuccFlag': this.onlySuccFlag
            };
            $.post("http://localhost:5000/api/ip/lookup", JSON.stringify(req), function(ret){
                ret.forEach(function(element) {
                    app_ip.ansList.push({
                        ip: element.ip,
                        status: element.statusinfo,
                        retClass: element.statusFlag
                    })
                }, this);
            });
        },
        pullSpecContent: function() {
            // 用于请求页面内容的方法，暂时保留。
            $.post("/getresponse", function(ret){
                // console.log(this.url);
                app_ip.spec = ret;
                // console.log(typeof(this.spec));
            })
        }
    }
})

var app_domain = new Vue({
    el: '#domain',
    data: {
        url: "",
        // todo: domainList 修改控件格式
        // 从文件导入，多行选框+单行添加或删除控件
        // 大小可以固定。
        //
        // 当前版本下，domainList需要通过js方法加以处理成Array
        // 后，json化传给后台
        domainList: "",
        spec: "",
        onlySuccFlag: true,
        ansList:  []
    },
    methods: {
        doDomainLookup: function() {
            // todo: 异步请求、异步返回
            this.ansList = [];
            req = {
                'url': this.url,
                'domainList': this.domainList.split('\n'),
                'spec': this.spec,
                'onlySuccFlag': this.onlySuccFlag
            };
            $.post("http://localhost:5000/api/domain/lookup", JSON.stringify(req), function(ret){
                ret.forEach(function(element) {
                    app_domain.ansList.push({
                        domain: element.domain,
                        status: element.statusinfo,
                        retClass: element.statusFlag
                    })
                }, this);
            });
        }
    }
})