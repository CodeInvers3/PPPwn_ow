var appView = Backbone.View.extend({
    el: '#app-v-pppwn',
    template: _.template($('#appWeb').html()),
    initialize: function(){
        var self = this;
        var params = new URLSearchParams({
            task:'adapters',
            token:'token_id'
        });
        fetch('/cgi-bin/wpwn.cgi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params.toString(),
        }).then(function(response){
            if(response.ok){
                return response.text();
            }else{
                throw new Error("Error cannot execute task.");
            }
        })
        .then(function(data){
            var interfaces = data.replace(/\[\+\] PPPwn\+\+ - PlayStation 4 PPPoE RCE by theflow|\[\+\] interfaces:|\r| \r/gi, function(value){
                return "";
            });
            self.interfaces(interfaces.split("\n"));
        })
        .catch(function(error){
            $('#task-log').find('.view').append(error+'<br>');
        });
        this.data = {
            interfaces: [],
            firmware: [
                {"version":"11.00","value":"1100"},
                {"version":"10.00","value":"1000"},
                {"version":"9.00","value":"900"},
                {"version":"7.50","value":"750"},
                {"version":"7.00","value":"700"}
            ]
        }
        this.render();
    },
    interfaces: function(data){
        var list = [];
        data.forEach(function(value){
            if(value){
                list.push(value.trim());
            }
        });
        this.data.interfaces = list;
        this.render();
    },
    render: function(){
        this.$el.html(this.template(this.data));
        return this;
    },
    events: {
        'click #id_run': function(){

            var path = this.$el.find('[name=path]');
            var adapter = this.$el.find('[name=adapter]');
            var firmware = this.$el.find('[name=firmware]');

            var params = new URLSearchParams({
                task:'run',
                token:'token_id',
                path:path.val(),
                adapter:adapter.val(),
                firmware:firmware.val()
            });
            fetch('/cgi-bin/wpwn.cgi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: params.toString(),
            }).then(function(response){
                if(response.ok){
                    return response.text();
                }else{
                    throw new Error("Error cannot execute task.");
                }
            })
            .then(function(text){
                $('#task-log').find('.view').append(text).append('<br>');
            })
            .catch(function(error){
                $('#task-log').find('.view').append(error+'<br>');
            });
        },
        'click #id_stop': function(){
            var params = new URLSearchParams({
                task:'stop',
                token:'token_id'
            });
            fetch('/cgi-bin/wpwn.cgi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: params.toString(),
            }).then(function(response){
                if(response.ok){
                    return response.text();
                }else{
                    throw new Error("Error cannot execute task.");
                }
            })
            .then(function(text){
                var output = $('#task-log').find('.view');
                output.append(text).append("<br>");
            })
            .catch(function(error){
                $('#task-log').find('.view').append(error+'<br>');
            });
        },
        'click #id_enable': function(){
            var params = new URLSearchParams({
                task:'enable',
                token:'token_id'
            });
            fetch('/cgi-bin/wpwn.cgi', {
                method: 'POST',
                body: params.toString(),
            }).then(function(response){
                if(response.ok){
                    return response.text();
                }else{
                    throw new Error("Error cannot execute task.");
                }
            })
            .catch(function(error){
                $('#task-log').find('.view').append(error+'<br>');
            })
            .then(function(text){
                var output = $('#task-log').find('.view');
                output.append(text).append("<br>");
            });
        }
    }
});
new appView();