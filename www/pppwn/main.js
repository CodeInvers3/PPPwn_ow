var Pwg = Backbone.Model.extend({
    urlRoot: '/cgi-bin/pw.cgi',
    defaults: {
        update: false,
        pppoe: '',
        pppwn: false,
        compiles: [],
        pppwned: false,
        running: false,
        autorun: false,
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

                button.prop('task', 'start').addClass('active').text('Execute');

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

            self.textareaOut.append("Awaiting response\n");

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
                    timeout:this.inputTimeout.val()
                }
            }).then(function(response){
                if(response.output){
                    self.textareaOut.append(response.output+"\n");
                }
                button.prop('task', 'start').addClass('active').text('Execute');
            }).catch(function(err, textStatus, errorThrown){
                if(err.responseJSON) self.textareaOut.append(err.responseJSON.output+"\n");
                if(err.textStatus) self.textareaOut.append(err.textStatus+"\n");
                button.prop('task', 'start').addClass('active').text('Execute');
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
                    version:this.inputVersion.val()
                }
            }).then(function(response){
                if(response.output){
                    self.textareaOut.append(response.output+"\n");
                }
            }).catch(function(err){
                self.textareaOut.append(err.responseJSON.output+"\n");
            });

        },
        'click button#switch_pw': function(event){

            var self = this;
            var button = $(event.target);
            var task = button.prop('task');

            if(task == 'disable'){
                button.prop('task', 'enable').text('Enable autorun');
            }else
            if(task == 'enable'){

                if(!this.inputRoot.val() || !this.inputAdapter.val() || !this.inputVersion.val()){
                    $.modal(function (modal) {
                        modal.content(self.templates.msg({message: 'Interface and firmware are required to enable autorun'}));
                    });
                    return;
                }

                button.prop('task', 'disable').text('Disable autorun');

            }
            
            this.model.fetch({
                method: 'POST',
                data: {
                    task:task,
                    token:this.webToken,
                    root:this.inputRoot.val(),
                    stage1:this.stage1[this.inputVersion.val()],
                    stage2:this.stage2[this.inputVersion.val()],
                    timeout:this.inputTimeout.val(),
                    adapter:this.inputAdapter.val(),
                    version:this.inputVersion.val()
                }
            }).then(function(response){
                if(response.output){
                    self.textareaOut.append(response.output+"\n");
                }
            }).catch(function(err){
                self.textareaOut.append(err.responseJSON.output+"\n");
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
                $.modal.content(self.templates.msg({message: err.responseJSON.output}));
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
                $.modal.content(self.templates.msg({message: err.responseJSON.output}));
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
                self.textareaOut.append(res.output+"\n");
            }).catch(function(){
                self.textareaOut.append("error\n");
            });
        }
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

        var res = pwg.fetch({
            method: 'POST',
            data: {
                task:'state',
                token:this.webToken
            },
            success: this.render.bind(this),
            error: function(err){
                return  err.responseJSON ? err.responseJSON.message : 'Unknow issue';
            }
        });

        if(typeof callback == 'function'){
            res.then(callback);
        }

        res.catch(function(err) {
            $.modal(function(modal){
                modal.content(self.templates.msg({message: err.responseJSON.output}));
            });
        });

    },
    render: function(response){

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
        
        response.set('interfaces', interfaces);

        var data = response.toJSON();

        this.$el.html(this.templates.web(data));

        this.webToken = this.cookie('token');
        this.stage1 = data.stage1;
        this.stage2 = data.stage2;
        this.textareaOut = this.$('#task-log .output');
        this.buttonAction = this.$('button#action_pw');
        this.buttonSwitch = this.$('button#switch_pw');
        this.buttonUpdate = this.$('button#update_rep');
        this.buttonInstall = this.$('button#install_pw');
        this.inputRoot = this.$('[name=root]');
        this.inputTimeout = this.$('[name=timeout]');
        this.inputAdapter = this.$('[name=adapter]');
        this.inputVersion = this.$('[name=version]');
        this.inputOption = this.$('[name=option]');
        this.inputConnect = this.$('[id=pppoe_pw]');

        if(this.model.get('running')){
            this.buttonAction.prop('task', 'stop').text('Stop');
        }else{
            this.buttonAction.prop('task', 'start').text('Execute');
        }

        if(this.model.get('autorun')){
            this.buttonSwitch.prop('task', 'disable').text('Disable autorun');
        }else{
            this.buttonSwitch.prop('task', 'enable').text('Enable autorun');
        }

        if(this.model.get('update')){
            $.modal(function(modal){
                modal.content(self.templates.msg({message: 'Update available'}));
            });
        }
        
        return this;

    },
    initialize: function(){

        var self = this;
        this.loading = this.$('#loading_ide');
        this.state();

        $('a#credits').click(function(){
            $.modal(function(modal){
                modal.content(self.templates.msg({message: 'TheOfficialFloW / SiSTR0 / xfangfang'}));
            });
        });

    }
});

new appView({
    model: pwg,
    el: '#appWeb'
});