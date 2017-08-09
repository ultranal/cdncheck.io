## One-Page CDNCheck.io API说明

### 说明
所有API全部接收json参数，并返回json。
所有的数据绑定和前端逻辑在vue.js实现的ViewModel层完成，后端只负责数据处理，
不执行任何与前端相关的代码或提供任何页面。


### 总路由 /api
#### ip : 域名查ip模块

    lookup : 执行查询
    接收4个参数:hostname, iprange, spec, onlySuccFlag
        string hostname: 目标页的URL（包含主机名和协议头、路径）
        string iprange: CIDR表示法表示的IP段
        string spec: 目标网页的特征内容
        bool onlySuccFlag: 设置是否只返回验证成功的内容，缺省为true
    返回一个由Ip段内所有IP的返回情况的Dict组成的Array
        string ip: IP地址
        bool status: 返回情况，验证成功为true
        string statusFlag: 可能为success, warning, ipError undefined。success代表校验成功，warning代表存在连接问题, undefined代表连接成功但校验失败, ipError代表IP段存在错误。
        string statusinfo: 提示信息
    
    pullRemoteContent: 拉取远程服务器响应，因过于危险而搁置。

#### domain : ip查域名模块 
    lookup : 执行查询
    接收4个参数: url, domainList, spec, onlySuccFlag
        string url: 目标位置的URL（即hostname字段的值）
        array domainList: 待检域名表
        string spec: 目标网页的特征内容
        bool onlySuccFlag: 设置是否只返回验证成功的内容，缺省为true
    返回一个由domainList内所有域名的返回情况的Dict组成的Array
        string domain: 域名
        bool status: 返回情况，验证成功为true
        string statusFlag: 可能为success, warning, undefined。success代表校验成功，warning代表存在连接问题, undefined代表连接成功但校验失败。