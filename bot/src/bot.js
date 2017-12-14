let env = require('node-env-file');
let filessystem = require('fs');
let os = require('os');
let spawn = require('child_process').spawn;
let python_shell = require('python-shell');

env(__dirname + '/.env');

let Botkit = require('botkit');

let controller = Botkit.slackbot({
    clientId: process.env.clientID,
    clientSecret: process.env.clientSecret,
    scopes: ['bot'],
    redirectUri: process.env.redirectUri,
    json_file_store: __dirname + '/.data/db/',
    debug: true,
    interactive_replies: true
});

controller.startTicking();

let bot = controller.spawn({
    token: process.env.token
}).startRTM();


controller.setupWebserver(3000, function (err, webserver) {
// Configure a route to receive webhooks from slack
    controller.createWebhookEndpoints(webserver);
    controller.createOauthEndpoints(webserver);
});

//auxiliar variable to control duplicate replies
let alreadySent = 1;

controller.on('direct_message', function(bot, message){
    let options = {
        mode: 'text',
        pythonPath: 'python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [message.text]
    };
    console.log(message.text);
    
    if(alreadySent == 0){
        alreadySent = 1;
        return;
    }
    alreadySent = 0;
    python_shell.run('script.py', options, function (err, results) {
        if (err) throw err;
        console.log('results: %j', results[0]);
        
        bot.reply(message, results[0]);
    });

})