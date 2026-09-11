// Local fixture regression test. Run: node verify.cjs
// Requires Playwright with Chromium installed. Optional TYPOGRAPHY_PLAYWRIGHT_PATH.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const pw = require(process.env.TYPOGRAPHY_PLAYWRIGHT_PATH || 'playwright');
const dir = __dirname;
const outputDir = path.resolve(__dirname, '../artifacts');
const baselineOnly = process.argv.includes('--baseline-only');
const configs = [
  {name:'before-320',file:'before.html',width:320,baseline:true},
  {name:'before-1440',file:'before.html',width:1440,baseline:true},
  ...[320,390,768,1440].map(width=>({name:`after-${width}`,file:'index.html',width})),
  {name:'after-320-text200',file:'index.html',width:320,textScale:2},
  {name:'after-768-text200',file:'index.html',width:768,textScale:2},
  {name:'after-390-serif',file:'index.html',width:390,serif:true},
  {name:'after-320-long',file:'index.html',width:320,dynamic:'long'},
  {name:'after-320-short',file:'index.html',width:320,dynamic:'short'},
];
(async()=>{
  const browser = await pw.chromium.launch({headless:true});
  fs.mkdirSync(path.join(outputDir,'screenshots'),{recursive:true});
  const results=[];
  for(const config of configs.filter(c=>!baselineOnly || c.baseline)) {
    const page=await browser.newPage({viewport:{width:config.width,height:1000},deviceScaleFactor:1});
    const errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto(pathToFileURL(path.join(dir,config.file)).href);
    await page.evaluate(()=>document.fonts.ready);
    if(config.textScale) await page.addStyleTag({content:`html{font-size:${config.textScale*100}% !important}`});
    if(config.serif) await page.addStyleTag({content:'body,button,input{font-family:Georgia,"Songti SC",serif !important}'});
    if(config.dynamic) await page.evaluate(mode=>{
      document.querySelector('#hero-title').textContent = mode==='short'?'已完成':'请在提交跨区域配送申请之前核对收件机构名称与联系地址，避免影响订单的正常送达。';
      document.querySelector('.card h3').textContent=mode==='short'?'杯':'适用于长途旅行与城市通勤的多功能防泼水可扩容双肩包（支持十六英寸电脑、独立湿物仓与可拆卸收纳配件套装）';
      document.querySelector('#address-error').textContent=mode==='short'?'请填写地址。':'收件地址不完整，请补充街道、门牌号及所在楼层；如无门牌号，请填写附近可识别的地标。当前配送区域暂不支持仅填写行政区名称，请核对联系人信息后重新提交。';
    },config.dynamic);
    const metrics=await page.evaluate(()=>{
      const linesOf=el=>{
        const lines=[]; const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
        while(walker.nextNode()) {
          const n=walker.currentNode;
          for(const {segment,index} of new Intl.Segmenter('zh',{granularity:'grapheme'}).segment(n.textContent)){
            const range=document.createRange();range.setStart(n,index);range.setEnd(n,index+segment.length);
            const r=range.getBoundingClientRect();if(!r.width||!r.height)continue;
            let line=lines.find(l=>Math.abs(l.top-r.top)<2);
            if(!line){line={top:r.top,text:''};lines.push(line);}line.text+=segment;
          }
        }
        return lines.sort((a,b)=>a.top-b.top).map(l=>l.text.trim()).filter(Boolean);
      };
      const clipping=[];
      for(const el of document.querySelectorAll('h1,h2,h3,p,button,td,th,label')){
        const r=el.getBoundingClientRect(),s=getComputedStyle(el);
        if(!r.width || !r.height) continue;
        if(el.scrollHeight>el.clientHeight+2 && ['hidden','clip'].includes(s.overflowY)) clipping.push({text:el.textContent.slice(0,60),reason:'vertical clipping'});
        const range=document.createRange();range.selectNodeContents(el);
        for(const t of range.getClientRects()) {
          if(t.bottom>r.bottom+3 || t.top<r.top-3) {
            clipping.push({text:el.textContent.slice(0,60),reason:'text outside element vertically'});break;
          }
        }
      }
      const titles=[...document.querySelectorAll('h1,h2,h3')].map(e=>({id:e.id||null,text:e.textContent,lines:linesOf(e)}));
      const punctuationLines=linesOf(document.querySelector('#punctuation'));
      const punctuationProblems=punctuationLines.filter(l=>/^[，。！？、；：）》」』】]/u.test(l)||/[（《「『【]$/u.test(l));
      const tableRegion=document.querySelector('#table-region');
      const root=document.documentElement;
      return {
        viewport:innerWidth,scrollWidth:root.scrollWidth,rootFontSize:getComputedStyle(root).fontSize,
        lang:root.lang,clipping,titles,punctuationLines,punctuationProblems,
        table:{width:tableRegion.clientWidth,scrollWidth:tableRegion.scrollWidth,overflowX:getComputedStyle(tableRegion).overflowX},
        url:document.querySelector('#url').textContent.trim(),
        token:document.querySelector('tbody tr td:nth-child(2)').textContent.trim(),
        missingAmount:document.querySelector('tbody tr:nth-child(2) td:nth-child(3)').textContent.trim(),
        features:{balance:CSS.supports('text-wrap','balance'),pretty:CSS.supports('text-wrap','pretty')},
      };
    });
    let keyboardChecks=null;
    if(!config.baseline) {
      await page.locator('#table-region').focus();
      const tableFocused=await page.locator('#table-region').evaluate(e=>e===document.activeElement);
      let tableScrollWorks=true;
      if(metrics.table.scrollWidth>metrics.table.width+1) {
        await page.keyboard.press('ArrowRight');
        try {await page.waitForFunction(()=>document.querySelector('#table-region').scrollLeft>0,{},{timeout:1000});}
        catch {tableScrollWorks=false;}
      }
      await page.keyboard.press('Tab');
      const inputReachable=await page.locator('#address').evaluate(e=>e===document.activeElement);
      await page.keyboard.press('Tab');
      const submitReachable=await page.locator('#submit-button').evaluate(e=>e===document.activeElement);
      await page.keyboard.press('Enter');
      keyboardChecks={tableFocused,tableScrollWorks,inputReachable,submitReachable};
      await page.locator('#table-region').evaluate(e=>e.scrollLeft=0);
      await page.evaluate(()=>document.activeElement.blur());
    }
    const assertions={
      noPageOverflow:metrics.scrollWidth<=config.width+1,
      noClippedText:metrics.clipping.length===0,
      chineseLanguage:metrics.lang.startsWith('zh'),
      punctuationSample:metrics.punctuationProblems.length===0,
      originalUrlPreserved:metrics.url==='https://example.com/orders/2026/09/11/ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?source=typography-test',
      originalTokenPreserved:metrics.token==='CN-20260911-AFTERSALES-0000000000000000123456789',
      missingAmountNotZero:metrics.missingAmount==='—',
      noRuntimeErrors:errors.length===0,
      ...(keyboardChecks?{keyboardAccess:Object.values(keyboardChecks).every(Boolean)}:{}),
      ...(!config.baseline&&!config.dynamic&&!config.textScale?{titleSemanticGrouping:!metrics.titles.find(t=>t.id==='hero-title').lines.some(l=>l==='一个数字。')}:{}),
    };
    await page.screenshot({path:path.join(outputDir,'screenshots',`${config.name}.png`),fullPage:true});
    if(['after-320','after-1440','after-320-text200','after-390-serif'].includes(config.name)) {
      for(const id of ['hero','article','products','form']) await page.locator(`#${id}`).screenshot({path:path.join(outputDir,'screenshots',`${config.name}-${id}.png`)});
    }
    results.push({config,assertions,pass:Object.values(assertions).every(Boolean),metrics,keyboardChecks,errors});
    console.log(`${config.name}: ${Object.entries(assertions).filter(([,v])=>!v).map(([k])=>k).join(', ')||'PASS'}`);
    await page.close();
  }
  const report={browser:await browser.version(),timestamp:new Date().toISOString(),method:'Chromium headless; local file; text200 changes root font size, NOT real browser zoom; serif swaps system font, NOT network-font testing.',results};
  fs.writeFileSync(path.join(outputDir,baselineOnly?'baseline-results.json':'results.json'),JSON.stringify(report,null,2));
  await browser.close();
  if(results.some(r=>!r.config.baseline&&!r.pass))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
