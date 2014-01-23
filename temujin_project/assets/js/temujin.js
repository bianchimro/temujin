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
    
    temujin.executeOp = function(url, ns, data){

        data = data || {};
        data['__namespace__'] = ns;

        return $.ajax({
            method:'post',
            url : url,
            data : data,
        });
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
        self.params = {};
        self.inputs = {};
        self.descriptor = null;

        self.getDescriptor = function(){
            return $.get(self.url);
        };

        

        self.param = function(name, value){
            if(buckets.isUndefined(value)){
                return self.params[name];
            } else {
                self.params[name] = value;
                return self;
            }
        };

        self.run = function(){

        };


        
        return self;
    };


    temujin.process = function(options){
        return new temujin.Process(options);
    };



    




    // Make it a NodeJS module.
    if (typeof module !== 'undefined') {
        module.temujin = temujin;
    }
}());