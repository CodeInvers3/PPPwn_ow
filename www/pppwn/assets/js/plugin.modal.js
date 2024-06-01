/*
 * Name: Modal plugin
 * Project: Modular
 * version: 0.5
 * email: manyandamariano@hotmail.com
 */

(function($){

    $.fn.modal = function(callback){

        $.modal.selector = this;
        $.modal.open(callback);

        return this;
    }

    $.modal = function(callback){

        $.modal.open(callback);
        return this;
        /*
        se debe arreglar esta opcion
        if(typeof options == 'object'){

            var selector = $(options.selector);

            if(selector.length){

                options = $.extend({
                    selector: selector,
                    url: options.selector.val(),
                    data: options.selector.data(),
                    open: $.modal.open
                }, options);
    
            }

            this.options = options;

        }

        return this;*/

    }

    $.modal.open = function(callback){
        
        this._open = callback;

        if(!$(document.body).find('.modal-background').length){

            this._background = $(document.createElement('div')).addClass('modal-background');
            this._container = $(document.createElement('div')).addClass('modal-container');
            this._content = $(document.createElement('div')).addClass('modal-content');

            this._background.append(this._container.append(this._content));

            callback(this);

        }

        if(typeof callback == 'function'){

            if(this._background){
                $(document.body).data('noscroll', 1)
                .append(this._background.css({opacity:0})
                .animate({opacity:1}, 300));
            }

        }

        return this;
    }

    $.modal.content = function(html_content){

        if(this._content.length){
            this._content.html(html_content);
        }

    }

    $.modal.loading = function(html_text){

        if(this._content.length){

            this._waiting = $(document.createElement('div')).addClass('modal-waiting')
            .html($(document.createElement('div')).addClass('modal-loading-icon'));
            this._content.append(this._waiting);

        }

    }

    $.modal.close = function(time = 150){

        if($(document.body).data('noscroll')){
            
            if(this._background.length){

                this._background.animate({opacity:0}, time, function(){
                    $(this).remove();
                })

            }
            
        }

    }
 
}(jQuery));