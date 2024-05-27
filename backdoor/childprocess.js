const  {exec} = require('child_process');

exec('cat .env', (err, stdout, stderr) => {
  if(err) throw err
  if(stderr) return console.log(`Execution error: ${stderr}`)
  console.log(`Env file content:  ${stdout}`)
})
