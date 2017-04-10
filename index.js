const faker = require('faker');
const fs = require('fs');
const os = require('os');
const path = require('path');

const type = process.argv[2]
const amount = process.argv[3]
const output = process.argv[4]

function generateType(type, amount=100, output){
  if (output===undefined){
    output = type.replace(/\./g,'_');
  }

  const fakerMethod = type.split('.').reduce((res, cur)=>{
    return res?res[cur]:res;
  },faker);

  amount = parseInt(amount)

  //create file
  let stream = fs.createWriteStream(path.join(__dirname, 'output', `${output}.csv`));

  for (let i=0;i<amount;i++){
    const val = fakerMethod.apply(fakerMethod);
    stream.write(val.toString());
    stream.write(os.EOL);
  }
  stream.end();
}

function init(type, amount, output){
  const DEFAULT_TYPES = [
    // 'address.city',
    // 'address.state',
    // 'address.latitude',
    // 'address.longitude',

    // 'commerce.price',
    // 'commerce.product',
    // 'commerce.productMaterial',
    // 'company.companyName',
    // 'date.past',

    // 'finance.amount',
    // 'image.image',
    // 'image.imageUrl',
    // 'image.dataUri',
    // 'internet.email',
    // 'internet.userName',
    // 'internet.protocol',
    // 'internet.url',
    // 'internet.ip',
    // 'internet.ipv6',
    // 'internet.password',
    // 'lorem.text',
    // 'name.firstName',
    // 'name.lastName',
    // 'name.jobTitle',
    // 'phone.phoneNumber',
    'random.uuid',
    'system.fileName',
  ];
  if (type==='*'){
    /*
az
cz
de
de_AT
de_CH
en
en_AU
en_BORK
en_CA
en_GB
en_IE
en_IND
en_US
en_au_ocker
es
es_MX
fa
fr
fr_CA
ge
id_ID
it
ja
ko
nb_NO
nep
nl
pl
pt_BR
ru
sk
sv
tr
uk
vi
zh_CN
zh_TW
    */
    // faker.locale =

    DEFAULT_TYPES.forEach((type, index, allTypes)=>{
      // setTimeout(()=>{
        generateType(type,amount);
        console.log(`${Math.round((index+1)/allTypes.length*100)}% complete`);
      // })
    });
  }else{
    generateType(type,amount,output);
  }
}

init(type, amount, output);
