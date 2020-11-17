const request = require('request');
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function main(){
    area = "jingkaiqub"
    years = [...Array(10).keys()].map(i=>(i+2011).toString())
    for (let idx = 0; idx < years.length; idx++) {
        var url = 'https://www.anjuke.com/fangjia/hf'+ years[idx]+'/'+area;
        const resp = await axios.get(url);
        const $ = cheerio.load(resp.data);
        const date = [];
        const price = [];
        $(".nostyle b").each(function(i, e) {
            var item = $(e).text();
            var year = (item.match(/(\d{4})年/)[1]), 
                month = (item.match(/年(\d{2})月/)[1]);
            date.push(year+"  "+month);
        });
        $(".nostyle span").each(function(i, e) {
            var item = $(e).text();
            var p = (item.match(/\d+/)[0]);
            price.push(p);
        });

        fname = area + ".data";
        var stream = fs.createWriteStream(fname, {flags:'a'});
        for (let i = 0; i < date.length; i++) {
            stream.write(date[i]+"  "+price[i] + "\n");
        }  
    }
    
}
    
main()


