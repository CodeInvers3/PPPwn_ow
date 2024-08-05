var Pwg = Backbone.Model.extend({
    urlRoot: '/cgi-bin/pw.cgi',
    defaults: {
        chipname: '',
        update: false,
        pppoe: '',
        pppwn: true,
        compiled: [],
        pppwned: false,
        running: false,
        autorun: false,
        root: '',
        interfaces: [],
        timeout: 0,
        version: '',
        versions: [],
        stage1: {},
        stage2: {},
        theme: 'default',
        adapter: ''
    }
});

var SectionRouter = Backbone.Router.extend({
    templates: {
        payload: _.template($('#payloadTpl').html())
    },
    routes: {
        'payloads': 'payloads'
    },
    payloads: function(){
        
        var self = this,uname = document.location.hash.replace("#/","");
        
        $.modal(function(modal){
            modal.content($('<div class="preloader center"></div>'));
        });
        $.get(`pppwn/payloads.json`, function(data){
            $.modal.close();
            $('#appWeb').html(self.templates.payload(data));
        });
    }
});

var pwg = new Pwg();
var appView = Backbone.View.extend({
    templates: {
        web: _.template($('#webTpl').html()),
        msg: _.template($('#msgTpl').html())
    },
    events: {
        'click button#action_pw': function(event){

            var self = this;
            var button = $(event.target);
            var task = button.prop('task');

            if(task == 'stop'){

                button.prop('task', 'start').addClass('active').text('Start');

            }else
            if(task == 'start'){

                if(!this.inputRoot.val() || !this.inputAdapter.val() || !this.inputVersion.val()){
                    $.modal(function (modal) {
                        modal.content(self.templates.msg({message: 'Interface and firmware are required to execute.'}));
                    });
                    return;
                }
                
                button.prop('task', 'stop').removeClass('active').text('Stop');

            }

            $.modal(function(modal){
                modal.content($('<div class="preloader center"></div>'));
            });

            this.model.fetch({
                method: 'POST',
                data: {
                    task:task,
                    token:this.webToken,
                    root:this.inputRoot.val(),
                    adapter:this.inputAdapter.val(),
                    version:this.inputVersion.val(),
                    stage1:this.stage1[this.inputVersion.val()],
                    stage2:this.stage2[this.inputVersion.val()],
                    timeout:this.inputTimeout.val(),
                    auto:this.selectAuto.val()
                }
            }).then(function(response){
                $.modal.close();
                button.prop('task', 'start').addClass('active').text('Start');
            }).catch(function(err, textStatus, errorThrown){
                if(err.responseJSON){
                    $.modal.content(self.templates.msg({message: err.responseJSON.output}));
                }else{
                    $.modal.content(self.templates.msg({message: err.responseText}));
                }
                button.prop('task', 'start').addClass('active').text('Start');
            });

        },
        'click button#params_pw': function(event){

            var self = this;

            if(!this.inputRoot.val() || !this.inputTimeout.val() || !this.inputAdapter.val() || !this.inputVersion.val()){
                $.modal(function (modal) {
                    modal.content(self.templates.msg({message: 'Required options fields.'}));
                });
                return;
            }

            $.modal(function (modal) {
                modal.content($('<div class="preloader center"></div>'));
            });
            
            this.model.fetch({
                method: 'POST',
                data: {
                    task:'params',
                    token:this.webToken,
                    root:this.inputRoot.val(),
                    stage1:this.stage1[this.inputVersion.val()],
                    stage2:this.stage2[this.inputVersion.val()],
                    timeout:this.inputTimeout.val(),
                    adapter:this.inputAdapter.val(),
                    version:this.inputVersion.val(),
                    auto:this.selectAuto.val()
                }
            }).then(function(response){
                if(response.output){
                    $.modal.content(self.templates.msg({message: response.output}));
                }
                $.modal.close();
            }).catch(function(err){
                if(err.responseJSON){
                    $.modal.content(self.templates.msg({message: err.responseJSON.output}));
                }else{
                    $.modal.content(self.templates.msg({message: err.responseText}));
                }
                
            });

        },
        'click button#update_rep': function(event){

            var self = this;

            $.modal(function(modal){
                modal.content($('<div class="preloader center"></div>'));
            });
            
            this.model.fetch({
                method: 'POST',
                data: {
                    task:'update',
                    token:this.webToken
                },
                success: this.state.bind(this)
            }).then(function(){
                document.cookie = 'token=; path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                $.modal.close();
            }).catch(function(err){
                $.modal.content(self.templates.msg({message: err.responseJSON.output}));
            });

        },
        'click button#install_pw': function(event){

            var self = this;

            if(!this.inputOption.val()) return;

            this.buttonInstall.attr('disabled');

            $.modal(function(modal){
                modal.content($('<div class="preloader center"></div>'));
            });

            this.model.fetch({
                method: 'POST',
                data: {
                    task:'setup',
                    token:this.webToken,
                    option:this.inputOption.val()
                }
            }).then(function(){
                self.state(function(){
                    $.modal.close();
                });
            }).catch(function(err){
                if(err.responseJSON){
                    $.modal.content(self.templates.msg({message: err.responseJSON.output}));
                }else{
                    $.modal.content(self.templates.msg({message: err.responseText}));
                }
                
            });

        },
        'click button#remove_rep': function(){

            var self = this;

            $.modal(function(modal){
                modal.content($('<div class="preloader center"></div>'));
            });

            this.model.fetch({
                method: 'POST',
                data: {
                    task:'remove',
                    token:this.webToken
                }
            }).then(function(res){
                location.assign("/");
            }).catch(function(err){
                if(err.responseJSON){
                    $.modal.content(self.templates.msg({message: err.responseJSON.output}));
                }else{
                    $.modal.content(self.templates.msg({message: err.responseText}));
                }
                
            });

        },
        'click button#pppoe_pw': function(){
            var self = this;
            this.model.fetch({
                method: 'POST',
                data: {
                    task:'connect',
                    token:this.webToken,
                    status:this.inputConnect.val()
                }
            }).then(function(res){
                
                var status = self.model.get('pppoe');

                if(status == 'running'){
                    self.inputConnect.text('PPPoe stop').val()
                }else
                if(status == 'inactive'){
                    self.inputConnect.text('PPPoe start').val(status)
                }
                $.modal(function(modal){
                    modal.content(self.templates.msg({message: res.output}));
                });
            }).catch(function(err){
                $.modal(function(modal){
                    if(err.responseJSON){
                        modal.content(self.templates.msg({message: err.responseJSON.output}));
                    }else{
                        modal.content(self.templates.msg({message: err.responseText}));
                    }
                });
            });
        },
        'click button.sent-payload': function(event){

            var selector = $(event.target);

            $.modal(function(modal){
                modal.content($('<div class="preloader center"></div>'));
            });
            
            var self = this;
            this.ajax({
                method: 'POST',
                url: 'http://127.0.0.1:9090/status',
            }).done(function(req){

                var res = JSON.parse(req.responseText);
                if(res.status == 'ready'){
                    
                    self.ajax({
                        method: 'GET',
                        url: selector.val(),
                        responseType: 'arraybuffer'
                    }).done(function(req){

                        if((req.status === 200 || req.status === 304) && req.response){
                            
                            self.ajax({
                                method: 'POST',
                                url: 'http://127.0.0.1:9090',
                                async: true,
                                data: req.response
                            }).done(function(event){

                                if(req.status === 200){
                                    $.modal.content(self.templates.msg({message: 'Payload loaded'}));
                                    $.modal.close();
                                }else{
                                    $.modal.content(self.templates.msg({message: 'Cannot send payload'}));
                                    $.modal.close();
                                    return;
                                }

                            }).fail(function(){
                                $.modal.content(self.templates.msg({message: 'Cannot Load Payload Because The BinLoader Server Is Busy'}));
                            });

                        }

                    });
                }

            }).fail(function(err){
                $.modal.content(self.templates.msg({message: 'Cannot Load Payload Because The BinLoader Server Is Not Running'}));
            });

        }
    },
    ajax: function(options){
                    
        var req = new XMLHttpRequest();
        
        if(typeof options.async == 'boolean'){
            req.open(options.method, options.url, options.async);
        }else{
            req.open(options.method, options.url);
        }

        if(options.responseType){
            req.responseType = options.responseType;
        }

        req.onload = function() {
            if (req.status >= 200 && req.status < 300) {
                if (typeof options.success === 'function') {
                    options.success(req);
                }
            } else {
                if (typeof options.error === 'function') {
                    options.error(req.statusText);
                }
            }
        };
        
        req.onerror = function() {
            if (typeof options.error === 'function') {
                options.error(req.statusText);
            }
        };

        req.send(options.data ? options.data : null);
        
        return {
            done: function(callback){
                options.success = callback;
                return this;
            },
            fail: function(callback){
                options.error = callback;
                return this;
            }
        };
    },
    cookie: function(name, value = null){

        if(value){
            document.cookie = `${name}=${value}; path=/`;
        }else{
            var cookies = document.cookie.split('; ');
            var info = {};
            for (var index in cookies) {
                var parts = cookies[index].split('=');
                info[parts[0]] = parts[1];
            }
            return info[name];
        }

    },
    state: function(callback){

        $.modal(function(modal){
            modal.content($('<div class="preloader center"></div>'));
        });

        var self = this, res = pwg.fetch({
            method: 'POST',
            data: {
                task:'state',
                token:this.webToken
            },
            error: function(err){
                return  err.responseJSON ? err.responseJSON.message : 'Unknow issue';
            }
        });

        if(typeof callback == 'function'){
            res.then(callback);
        }

        res.catch(function(err) {
            if(err.responseJSON){
                $.modal.content(self.templates.msg({message: err.responseJSON.output}));
            }else{
                $.modal.content(self.templates.msg({message: err.responseText}));
            }
                
        });
        

    },
    render: function(response){

        $.modal.close();

        var self = this, interfaces = [];

        if (this.model.get('stored_token')) {
            document.cookie = 'token=; path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
            this.cookie('token', this.model.get('stored_token'));
        }

        $.each(response.get('interfaces'), function(index, item){
            if(item.adapter != "[+] PPPwn++ - PlayStation 4 PPPoE RCE by theflow" && item.adapter != "[+] interfaces:"){
                interfaces.push(item);
            }
        });

        var data = response.toJSON();
        data.interfaces = interfaces;

        this.$el.html(this.templates.web(data));

        this.webToken = this.cookie('token');
        this.stage1 = data.stage1;
        this.stage2 = data.stage2;
        this.textareaOut = this.$('#task-log .output');
        this.buttonAction = this.$('button#action_pw');
        this.selectAuto = this.$('select#switch_pw');
        this.buttonUpdate = this.$('button#update_rep');
        this.buttonInstall = this.$('button#install_pw');
        this.inputRoot = this.$('[name=root]');
        this.inputTimeout = this.$('[name=timeout]');
        this.inputAdapter = this.$('[name=adapter]');
        this.inputVersion = this.$('[name=version]');
        this.inputOption = this.$('[name=option]');
        this.inputConnect = this.$('[id=pppoe_pw]');

        $('select#select-ifc').find('option').each(function(index, item){
            if(data.adapter == $(item).val()){
                $(item).addClass('op-selected');
            }else{
                $(item).removeClass('op-selected');
            }
        });

        $('select#select-fw').find('option').each(function(index, item){
            if(data.version == $(item).val()){
                $(item).addClass('op-selected')
            }else{
                $(item).removeClass('op-selected');
            }
        });

        if(this.model.get('running')){
            this.buttonAction.prop('task', 'stop').text('Stop');
        }else{
            this.buttonAction.prop('task', 'start').text('Start');
        }

        if(this.model.get('autorun')){
            this.selectAuto.val(1);
        }else{
            this.selectAuto.val(0);
        }

        if(this.model.get('update')){
            $.modal(function(modal){
                modal.content(self.templates.msg({message: 'Update available'}));
            });
        }

        $('a#credits').click(function(){
            $.modal(function(modal){
                modal.content(self.templates.msg({message: 'TheOfficialFloW / SiSTR0 / xfangfang'}));
            });
        });
        
        return this;

    },
    initialize: function(){

        this.loading = this.$('#loading_ide');
        this.state();
        this.listenTo(this.model, 'change', this.render);

    }
});

new appView({
    model: pwg,
    el: '#appWeb'
});

var sectionRouter = new SectionRouter();
Backbone.history.start();