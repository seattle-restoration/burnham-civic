// Parse the leftwashington.org data into invoice entries
const entries = [
  {id:'LW-001',entity:'John I. Haas',type:'Closure',loc:'Yakima',jobs:12,taxLo:'$22K',taxHi:'$58K',sector:'Agriculture',year:'2026'},
  {id:'LW-002',entity:'Blazing Bagels',type:'Closure',loc:'Seattle/Redmond/Bellevue',jobs:30,taxLo:'$59K',taxHi:'$187K',sector:'Food & Beverage',year:'2026'},
  {id:'LW-003',entity:'Rise Baking Company',type:'Relocation',loc:'Kent to Utah',jobs:120,taxLo:'$192K',taxHi:'$719K',sector:'Food Manufacturing',year:'2026'},
  {id:'LW-004',entity:'Atlassian US',type:'Layoff',loc:'Bellevue',jobs:63,taxLo:'$464K',taxHi:'$464K',sector:'Tech',year:'2026'},
  {id:'LW-005',entity:'Agrimacs',type:'Closure',loc:'Chelan',jobs:145,taxLo:'$260K',taxHi:'$695K',sector:'Agriculture',year:'2026'},
  {id:'LW-006',entity:'CHS Northwest',type:'Downsizing',loc:'Whatcom County',jobs:57,taxLo:'$227K',taxHi:'$461K',sector:'Agriculture/Energy',year:'2026'},
  {id:'LW-007',entity:'C2 Technologies',type:'Layoff',loc:'Virtual (WA)',jobs:1,taxLo:'$6K',taxHi:'$6K',sector:'Tech',year:'2026'},
  {id:'LW-008',entity:'Refresco Beverages US',type:'Downsizing',loc:'Walla Walla',jobs:58,taxLo:'$93K',taxHi:'$261K',sector:'Beverage Mfg',year:'2026'},
  {id:'LW-009',entity:'Northwest Hardwoods',type:'Downsizing',loc:'Centralia',jobs:70,taxLo:'$126K',taxHi:'$336K',sector:'Lumber/Mfg',year:'2026'},
  {id:'LW-010',entity:'MicroVision',type:'Layoff',loc:'Redmond',jobs:49,taxLo:'$361K',taxHi:'$361K',sector:'Tech/Lidar',year:'2026'},
  {id:'LW-011',entity:'Doosan GridTech',type:'Layoff',loc:'Bellevue',jobs:18,taxLo:'$133K',taxHi:'$133K',sector:'Energy Tech',year:'2026'},
  {id:'LW-012',entity:'IPIC Theaters',type:'Downsizing',loc:'Redmond',jobs:64,taxLo:'$110K',taxHi:'$376K',sector:'Entertainment',year:'2026'},
  {id:'LW-013',entity:'CHS Northwest (Round 2)',type:'Layoff',loc:'Various WA',jobs:38,taxLo:'$152K',taxHi:'$152K',sector:'Agriculture/Energy',year:'2026'},
  {id:'LW-014',entity:'Peshastin Pear Packers',type:'Layoff',loc:'Peshastin',jobs:31,taxLo:'$56K',taxHi:'$56K',sector:'Agriculture',year:'2026'},
  {id:'LW-015',entity:'PeaceHealth',type:'Layoff',loc:'Various WA',jobs:94,taxLo:'$244K',taxHi:'$244K',sector:'Healthcare',year:'2026'},
  {id:'LW-016',entity:'Eddie Bauer',type:'Downsizing',loc:'Seattle',jobs:60,taxLo:'$118K',taxHi:'$375K',sector:'Retail/Apparel',year:'2026'},
  {id:'LW-017',entity:'Congdon Packing Company',type:'Layoff',loc:'Yakima',jobs:102,taxLo:'$163K',taxHi:'$163K',sector:'Food Processing',year:'2026'},
  {id:'LW-018',entity:'GMRI / Bahama Breeze',type:'Downsizing',loc:'Tukwila',jobs:93,taxLo:'$183K',taxHi:'$581K',sector:'Restaurant',year:'2026'},
  {id:'LW-019',entity:'International Paper Company',type:'Downsizing',loc:'Union Gap',jobs:102,taxLo:'$224K',taxHi:'$550K',sector:'Manufacturing',year:'2026'},
  {id:'LW-020',entity:'Expedia',type:'Layoff',loc:'Seattle',jobs:162,taxLo:'$1.2M',taxHi:'$1.2M',sector:'Tech/Travel',year:'2026'},
  {id:'LW-021',entity:'Meta Platforms',type:'Layoff',loc:'King County',jobs:331,taxLo:'$2.4M',taxHi:'$2.4M',sector:'Tech',year:'2026'},
  {id:'LW-022',entity:'Food Service Slicing / Crunch Pak',type:'Downsizing',loc:'Selah',jobs:101,taxLo:'$161K',taxHi:'$454K',sector:'Food Processing',year:'2026'},
  {id:'LW-023',entity:'SMBC Manubank',type:'Layoff',loc:'Various WA',jobs:5,taxLo:'$26K',taxHi:'$26K',sector:'Finance',year:'2026'},
  {id:'LW-024',entity:'Tessera',type:'Layoff',loc:'King County',jobs:1,taxLo:'$7K',taxHi:'$7K',sector:'Tech',year:'2026'},
  {id:'LW-025',entity:'Swedish Health Services',type:'Layoff',loc:'King/Snohomish',jobs:50,taxLo:'$130K',taxHi:'$130K',sector:'Healthcare',year:'2026'},
  {id:'LW-026',entity:'Doosan GridTech (Round 2)',type:'Layoff',loc:'Bellevue',jobs:24,taxLo:'$177K',taxHi:'$177K',sector:'Energy Tech',year:'2026'},
  {id:'LW-027',entity:'Packaging Corp of America',type:'Downsizing',loc:'Wallula',jobs:200,taxLo:'$439K',taxHi:'$1.1M',sector:'Manufacturing',year:'2026'},
  {id:'LW-028',entity:'Verizon',type:'Layoff',loc:'Various WA',jobs:165,taxLo:'$724K',taxHi:'$724K',sector:'Telecom',year:'2026'},
  {id:'LW-029',entity:'Providence Health & Services',type:'Layoff',loc:'Various WA',jobs:57,taxLo:'$148K',taxHi:'$148K',sector:'Healthcare',year:'2026'},
  {id:'LW-030',entity:'Nordstrom Credit Bank',type:'Layoff',loc:'Remote WA',jobs:9,taxLo:'$47K',taxHi:'$47K',sector:'Finance/Retail',year:'2026'},
  {id:'LW-031',entity:'Meteorcomm',type:'Layoff',loc:'Renton',jobs:49,taxLo:'$361K',taxHi:'$361K',sector:'Tech/Comms',year:'2026'},
  {id:'LW-032',entity:'Great Floors',type:'Downsizing',loc:'Various WA',jobs:58,taxLo:'$93K',taxHi:'$261K',sector:'Retail/Home',year:'2026'},
  {id:'LW-033',entity:'Rad Power Bikes',type:'Downsizing',loc:'Seattle',jobs:64,taxLo:'$189K',taxHi:'$494K',sector:'E-Bikes',year:'2026'},
  {id:'LW-034',entity:'Adams County Public Hospital',type:'Layoff',loc:'Ritzville',jobs:108,taxLo:'$280K',taxHi:'$280K',sector:'Healthcare',year:'2026'},
  {id:'LW-035',entity:'Microsoft',type:'Layoff',loc:'Washington State',jobs:3160,taxLo:'$24.2M',taxHi:'$54.4M',sector:'Tech',year:'2025'},
  {id:'LW-036',entity:'Amazon',type:'Layoff',loc:'Seattle/Bellevue',jobs:2100,taxLo:'$16.1M',taxHi:'$36.2M',sector:'Tech',year:'2025'},
  {id:'LW-037',entity:'Starbucks',type:'Layoff',loc:'Seattle HQ',jobs:1100,taxLo:'$6.3M',taxHi:'$14.2M',sector:'Food & Beverage',year:'2025'},
  {id:'LW-038',entity:'Starbucks Supply Chain',type:'Relocation',loc:'Seattle to Nashville',jobs:200,taxLo:'$1.1M',taxHi:'$2.5M',sector:'Food & Beverage',year:'2025'},
  {id:'LW-039',entity:'Amazon (Denny Triangle)',type:'Relocation',loc:'Denny Triangle Seattle',jobs:800,taxLo:'$6.2M',taxHi:'$13.9M',sector:'Tech',year:'2025'},
  {id:'LW-040',entity:'T-Mobile',type:'Layoff',loc:'Washington State',jobs:393,taxLo:'$3.0M',taxHi:'$6.8M',sector:'Telecom',year:'2025'},
  {id:'LW-041',entity:'Meta (2025)',type:'Layoff',loc:'Redmond/Seattle',jobs:331,taxLo:'$2.6M',taxHi:'$5.8M',sector:'Tech',year:'2025'},
  {id:'LW-042',entity:'Google',type:'Downsizing',loc:'Fremont Seattle',jobs:300,taxLo:'$2.3M',taxHi:'$5.2M',sector:'Tech',year:'2025'},
  {id:'LW-043',entity:'Expedia (2025)',type:'Layoff',loc:'Seattle',jobs:162,taxLo:'$1.3M',taxHi:'$2.9M',sector:'Tech/Travel',year:'2025'},
  {id:'LW-044',entity:'Oracle',type:'Layoff',loc:'Seattle',jobs:161,taxLo:'$1.2M',taxHi:'$2.7M',sector:'Tech',year:'2025'},
  {id:'LW-045',entity:'Smartsheet',type:'Layoff',loc:'Bellevue',jobs:120,taxLo:'$880K',taxHi:'$2.0M',sector:'Tech/SaaS',year:'2025'},
  {id:'LW-046',entity:'F5',type:'Layoff',loc:'Seattle/Liberty Lake',jobs:106,taxLo:'$800K',taxHi:'$1.8M',sector:'Tech',year:'2025'},
  {id:'LW-047',entity:'Avalara',type:'Relocation',loc:'Seattle to North Carolina',jobs:0,taxLo:'TBD',taxHi:'TBD',sector:'Tech/FinTech',year:'2025'},
  {id:'LW-048',entity:'Howard Schultz',type:'Relocation',loc:'Seattle to Miami',jobs:0,taxLo:'TBD',taxHi:'TBD',sector:'Coffee/Philanthropy',year:'2025'},
  {id:'LW-049',entity:'Moment (Marc Barros)',type:'Relocation',loc:'WA to Wyoming',jobs:0,taxLo:'TBD',taxHi:'TBD',sector:'E-Commerce',year:'2025'},
  {id:'LW-050',entity:'Seattle VC Firm ($3B)',type:'Relocation',loc:'Seattle to Las Vegas',jobs:0,taxLo:'TBD',taxHi:'TBD',sector:'Venture Capital',year:'2025'},
  {id:'LW-051',entity:'Blue Origin',type:'Layoff',loc:'Seattle',jobs:0,taxLo:'TBD',taxHi:'TBD',sector:'Aerospace',year:'2025'},
  {id:'LW-052',entity:'Payscale',type:'Relocation',loc:'Seattle to Boston',jobs:150,taxLo:'$1.1M',taxHi:'$2.5M',sector:'Tech/Data',year:'2025'},
  {id:'LW-053',entity:'Battelle / PNNL',type:'Layoff',loc:'Various WA',jobs:68,taxLo:'$163K',taxHi:'$163K',sector:'Research',year:'2025'},
  {id:'LW-054',entity:'The Skillet Group',type:'Downsizing',loc:'Seattle',jobs:47,taxLo:'$92K',taxHi:'$294K',sector:'Restaurant',year:'2025'},
  {id:'LW-055',entity:'Solgen Power / Purelight',type:'Downsizing',loc:'Various WA',jobs:71,taxLo:'$283K',taxHi:'$574K',sector:'Energy/Solar',year:'2025'},
];

// Total
let totalJobs = 0, totalTaxLo = 0, totalTaxHi = 0;
entries.forEach(e => {
  totalJobs += e.jobs;
  const lo = e.taxLo.replace(/[^0-9.]/g,'');
  const hi = e.taxHi.replace(/[^0-9.]/g,'');
  if(lo && lo!='TBD') totalTaxLo += parseFloat(lo) * (e.taxLo.includes('M')?1000000:1000);
  if(hi && hi!='TBD') totalTaxHi += parseFloat(hi) * (e.taxHi.includes('M')?1000000:1000);
});
console.log('Total entries:', entries.length);
console.log('Total jobs:', totalJobs.toLocaleString());
console.log('Tax lost range: $' + (totalTaxLo/1000000).toFixed(1) + 'M - $' + (totalTaxHi/1000000).toFixed(1) + 'M/yr');
console.log(JSON.stringify(entries));
