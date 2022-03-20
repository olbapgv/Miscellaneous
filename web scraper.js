// # -*- coding: utf-8 -*-
// Short example of using javascript to retrieve web data when you do not have much more than a browser in your laptop.
//=============================================================================
//                          KEY FUNCTIONS
//=============================================================================

function wait(ms) {    
    return new Promise( w => setTimeout(w, ms) );    
    }
    
function navigate1( case1 ){
    var url = '<sample url>?parameter1=' + case1;
    $("html").load(url);
    }

function navigate2( case1, case2 ){
    var url = '<sample url>?parameter1=' + case1 + '&parameter2=' + case2;   
    $("html").load(url);
    }

// Let's store the html table as an array of arrays
function get_table(){
    data = document.getElementById('id').rows
    // Alternatively:
    // data = document.getElementsByTagName('table')[i].rows 
    // where i is the order of the table in the DOM
    lista = []
    for (var i=1; i < data.length; i++){
            celda = data[i].children
            fila = []            
            for (var j = 0; j < celda.length; j++) {
                fila.push(celda[j].innerText);            
                }
            if(fila.length > 3) { // Could really be any number that allows to filter useless columns
                lista.push(fila)
                }
            }
    return lista
    }

//=============================================================================
//                          Let's Load Jquery
//=============================================================================    

// Since javascript's console "resets" each time you navigate, we will
// use Jquery to solve this issue
var jq = document.createElement('script');
jq.src = 'https://code.jquery.com/jquery-3.3.1.min.js';
document.getElementsByTagName('head')[0].appendChild(jq)
jQuery.noConflict();
$.ajaxSetup({
    contentType: 'Content-type: text/plain; charset=iso-8859-1',
    beforeSend: function(temp) {
        temp.overrideMimeType('text/html;charset=iso-8859-1');
                }
    });


//=============================================================================
//                          Web scraping
//=============================================================================    

var columns = Array.from( ["c1", "c2", "..."]),
    category = [];
Array.from( document.getElementsByName('dropdown1')[0] ).forEach(i=>category.push( escape( i.value.trim() ) ) );
var results = [[columns]];
for (var i=1; i < category.length; i++) {
    var subcategory = [];
    await navigate1(category[i]);
    await wait(500);
    Array.from( document.getElementsByName('dropdown2')[0] ).forEach(z=>subcategory.push( escape( z.value.trim() ) ) );
    for (var j=1; j < subcategory.length; j++) {
        await navigate2( category[i], subcategory[j] );
        await wait(500);
        await results.push( get_table( unescape(category[i]) , unescape(subcategory[j]) ) )
        }
    }
var results = results.flat(1);

// Important: Adblock will block this download
let csv = 'data:text/csv;charset=utf-8,' + results.map(v=>v.join(';')).join('\n');
window.open( encodeURI(csv) );
