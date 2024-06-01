var state = Backbone.Model.extend({
    urlRoot: '/cgi-bin/pw.cgi',
    defaults: {
        running: false,
        active: false,
        interfaces: [],
        offsets: [],
        theme: 'default'
    }
});
var appView = Backbone.View.extend({
    el: '#app-v-pppwn',
    template: _.template($('#appWeb').html()),
    initialize: function(){
        var self = this;
        this.model = new state;
        this.listenTo(this.model, 'sync', this.render);
        this.model.fetch({
            method: 'POST',
            data: {
                task:'initialize',
                token:'token_id'
            }
        });
    },
    render: function(response){
        var self = this, interfaces = [];
        $.each(response.get('interfaces'), function(index, item){
            if(item.adapter != "[+] PPPwn++ - PlayStation 4 PPPoE RCE by theflow" && item.adapter != "[+] interfaces:"){
                interfaces.push(item);
            }
        });
        
        response.set('interfaces', interfaces);
        var data = response.toJSON();
        this.$el.html(this.template(data));

        if(response.get('running')){
            this.$('button#action_pw').addClass('active').prop('task', 'run').text('Stop');
        }
        
        if(data.output){
            console.log(data.output)
            this.$('#task-log .view').append(data.output+'<br>');
        }
        return this;
    },
    events: {
        'click button#action_pw': function(event){

            var selector = $(event.target);
            var output = $('#task-log').find('.view');
            var root = this.$el.find('[name=root]');
            var adapter = this.$el.find('[name=adapter]');
            var firmware = this.$el.find('[name=firmware]');

            if(selector.prop('task') == 'run'){

                output.append("Stopping process...<br>");
                selector.removeClass('active');
                selector.prop('task', 'stop').text('Stop');

            }else{

                if(!root.val() || !adapter.val() || !firmware.val()){
                    $.modal(function (modal) {
                        modal.loading('...');
                        modal.content($('<button class="md-close" type="button" onclick="$.modal.close();">X</button><p>Interface and firmware required.</p>'));
                    });
                    return;
                }

                output.append('Awaiting response...<br>');
                selector.addClass('active');
                selector.prop('task', 'run').text('Stop');

            }

            this.model.fetch({
                method: 'POST',
                data: {
                    task:selector.prop('task'),
                    token:'token_id',
                    root:root.val(),
                    adapter:adapter.val(),
                    firmware:firmware.val()
                }
            })
            .catch(function(err){
                output.append(err+'<br>');
            });

        },
        'click button#switch_pw': function(event){

            var selector = $(event.target);
            var root = this.$el.find('[name=root]');
            var adapter = this.$el.find('[name=adapter]');
            var firmware = this.$el.find('[name=firmware]');
            var task = 'enable';

            if(this.model.get('active')){
                task = 'disable';
            }else{

                if(!root.val() || !adapter.val() || !firmware.val()){
                    $.modal(function (modal) {
                        modal.content($('<button class="md-close" type="button" onclick="$.modal.close();">X</button><p>Interface and firmware required to activate.</p>'));
                    });
                    return;
                }

            }

            this.model.fetch({
                method: 'POST',
                data: {
                    task:task,
                    token:'token_id',
                    root:root.val(),
                    adapter:adapter.val(),
                    firmware:firmware.val()
                },
            })
            .catch(function(err){
                $('#task-log').find('.view').append(err+'<br>');
            });

        }
    }
});
new appView();