// Copyright 2014 Mauro Bianchi. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
//
// Some documentation is borrowed from the official Java API
// as it serves the same porpose.
/**
 * @namespace Top level namespace for Temujin client lib
 */
var temujin = {};
(function() {
    'use strict';


    temujin.watching = false;


    temujin.getNs = function(name){
        return $.ajax({
            method:'post',
            url : '/temujin/commands/getns/',
            data : {name:name},
        });                
    }

    
    temujin.describeOp = function(url){

        return $.get(url);

    };
    
    //TODO:remove
    temujin.executeOp = function(url, ns, data){

        data = data || {};
        data['__namespace__'] = ns;

        return $.ajax({
            method:'post',
            url : url,
            data : data,
        });
    };


    temujin.publish = function(topic, data){ 
        //console.log("ehy, got it", topic, data)
        return pubsub.publish(topic, data);

    };
    temujin.subscribe = function(topic, callback){ 
        return pubsub.subscribe(topic, function(topic, args){
            callback(args); 
        });
    };
    


    temujin.watch = function(){
        if (temujin.watching){return;}
        var ws = new WebSocket('ws://localhost:8000/ws/temujin_results?subscribe-broadcast&publish-broadcast');
        ws.onopen = function() {
            console.log("websocket connected");
        };
        ws.onmessage = function(e) {
            console.log("Received: " + e.data);
            var jsonData = JSON.parse(e.data);
            if(jsonData.token){
                console.log("received token publishing")
                setTimeout(function(){
                temujin.publish(jsonData.token, jsonData);
                }, 2000);
            }
        };
        ws.onerror = function(e) {
            console.error(e);
        };
        ws.onclose = function(e) {
            console.log("connection closed");
        }
    };



    temujin.Provider = function(baseUrl){
        var self = this;
        self.baseUrl = baseUrl;
        return self;

    };

    
    temujin.provider = function(baseUrl){
        return new temujin.Provider(baseUrl);
    };



    temujin.Process = function(url){
        var self = this;

        self.url = url;
        self.args = {};
        self.descriptor = null;

        self.getDescriptor = function(){
            return $.get(self.url);
        };

        

        self.arg = function(name, value){
            if(buckets.isUndefined(value)){
                return self.args[name];
            } else {
                self.args[name] = value;
                return self;
            }
        };


        self.run = function(){

            var data = $.extend(true, {}, self.args );
            console.log("eee", self.args)
            
            //using the deferred api, preparing for async
            var dfd = new jQuery.Deferred();

            $.ajax({
                method:'post',
                url : self.url,
                data : data,
            }).then(function(data){
                var token = data.token;
                token = token;
                //console.log("got token", token, data);
                var r = temujin.subscribe(token, function(wsData){
                    console.log("sub")
                    dfd.resolve(wsData);    
                    pubsub.unsubscribe(r);
                
                })
                //console.log("r", r)

                
            });

            return dfd.promise();

        };

        
        return self;
    };


    temujin.process = function(options){
        return new temujin.Process(options);
    };



    
    temujin.watch();



    // Make it a NodeJS module.
    if (typeof module !== 'undefined') {
        module.temujin = temujin;
    }
}());