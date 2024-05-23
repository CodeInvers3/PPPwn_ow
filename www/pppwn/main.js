var appView = Backbone.View.extend({
    el: '#app-v-pppwn',
    template: _.template($('#appWeb').html()),
    initialize: function(){
        var self = this;
        var params = new URLSearchParams({
            task:'adapters',
            token:'token_id'
        });
        fetch('/cgi-bin/pw.cgi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params.toString(),
        }).then(function(response){
            if(response.ok){
                return response.json();
            }else{
                throw new Error("Error cannot execute task.");
            }
        })
        .then(function(dataList){
            self.interfaces(dataList);
        })
        .catch(function(error){
            $('#task-log').find('.view').append(error+'<br>');
        });
        this.data = {
            interfaces: [],
            firmware: [
                {"version":"7.00","value":"700"},
                {"version":"7.50","value":"750"},
                {"version":"8.00","value":"800"},
                {"version":"8.50","value":"850"},
                {"version":"9.00","value":"900"},
                {"version":"9.03","value":"903"},
                {"version":"9.50","value":"950"},
                {"version":"10.00","value":"1000"},
                {"version":"10.50","value":"1050"},
                {"version":"11.00","value":"1100"}
            ]
        }
        this.render();
    },
    interfaces: function(data){
        var list = [];
        data.forEach(function(value, index){
            if(index > 1){
                list.push(value);
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

            var root = this.$el.find('[name=root]');
            var adapter = this.$el.find('[name=adapter]');
            var firmware = this.$el.find('[name=firmware]');

            var params = new URLSearchParams({
                task:'run',
                token:'token_id',
                root:root.val(),
                adapter:adapter.val(),
                firmware:firmware.val()
            });

            $('#task-log').find('.view').append('Awaiting response...<br>');

            fetch('/cgi-bin/pw.cgi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: params.toString(),
            }).then(function(response){
                if(response.ok){
                    return response.json();
                }else{
                    throw new Error("Error cannot execute task.");
                }
            })
            .then(function(data){
                $('#task-log').find('.view').append(data.output).append('<br>');
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

            fetch('/cgi-bin/pw.cgi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: params.toString(),
            }).then(function(response){
                if(response.ok){
                    return response.json();
                }else{
                    throw new Error("Error cannot execute task.");
                }
            })
            .then(function(data){
                var output = $('#task-log').find('.view');
                output.append("Stopping process...").append("<br>");
                output.append(data.output).append("<br>");
            })
            .catch(function(error){
                $('#task-log').find('.view').append(error+'<br>');
            });

        },
        'click #id_enable': function(){

            var root = this.$el.find('[name=root]');
            var adapter = this.$el.find('[name=adapter]');
            var firmware = this.$el.find('[name=firmware]');
            
            var params = new URLSearchParams({
                task:'enable',
                token:'token_id',
                root:root.val(),
                adapter:adapter.val(),
                firmware:firmware.val()
            });

            fetch('/cgi-bin/pw.cgi', {
                method: 'POST',
                body: params.toString(),
            }).then(function(response){
                if(response.ok){
                    return response.json();
                }else{
                    throw new Error("Error cannot execute task.");
                }
            })
            .catch(function(error){
                $('#task-log').find('.view').append(error+'<br>');
            })
            .then(function(data){
                var output = $('#task-log').find('.view');
                output.append(data.output).append("<br>");
            });

        }
    }
});
new appView();