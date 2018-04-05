var AWS = require('aws-sdk');
var lexruntime = new AWS.LexRuntime();
console.log("in handler function")
var lexUserId = 'chatbot' + Date.now();
var sessAttributes = {};

// if const doesn't work, rename the type to var
const callLex = (message) => {
  return new Promise((resolve, reject) => {
    var params = {
      botAlias: '$LATEST',
      /* required */
      botName: 'chatbot',
      /* required */
      inputText: message,
      /* required */
      userId: lexUserId,
      /* required */
      // requestAttributes: {
      //   '<String>': 'STRING_VALUE',
      //   /* '<String>': ... */
      // },
      sessionAttributes: sessAttributes
    };
    
    lexruntime.postText(params, function(err, data) {
      if (err) reject(err);
      else {
        sessAttributes = data.sessionAttributes;
        resolve(data); // successful response
      }
    });
  });
};

exports.handler = (event, context, callback) => {
    // TODO implement
    console.log("in handler function")
    callLex(event.message)
      .then((lexResponse) => {
        /* VALID RESPONSE */
        callback(null, lexResponse.message); // this is the Lambda callback
      })
      .catch((error) => {
        /* SOMETHING WENT WRONG */
        callback(error); // this is the Lambda callback
      });
};: "value1"
}