var app,
    resultPage,
    cols = 5,
    rows = 3,
    padding = 8,
    maxResults = 500,
    total_results = 0,
    bannerInIdx = 1,
    bannerOutIdx = 0,
    strokeIdx = 1,
    fadePerc = 0,
    results = [],
    Images = [],
    strokeColor = ['black', 'transparent'],
    searchColor = 'transparent',
    canvasColor = 'transparent';

/** Funções que controlam a animação do banner na página principal */
function setAnimation() {
    if(document.getElementById('animation').checked) {
        animation.On();
        alert("Banner animation is On!");
    } else {
        animation.Off();
        alert("Banner animation is Off!");
    }
}

var animation = (function() {
    var timedSwitch;

    function On() {
        timedSwitch = setInterval(switchLogo, 10000);
    }

    function Off() {
        clearInterval(timedSwitch);
    }
    return {
        On : On,
        Off : Off
    };
})();
/** */

/** Funções que controlam a criação de uma nova pesquisa */
/** Nova página de pesquisa */
function newSearchPage() {
    window.addEventListener('resize', initSearchPage, false);
    app = new SearchX();
}

/** Reinicializar a página de pesquisa no resize da mesma */
function initSearchPage() {
    app.refresh(bannerInIdx, 100);
}

/** Objeto que representa a aplicação multimédia na vertente de pesquisa *
 *
 * @constructor
 */
function SearchX() {
    this.canvas = document.getElementById("canvas");
    this.ctx = this.canvas.getContext("2d");
    this.canvas.addEventListener('click', switchLogo, false);
    this.banners = new AppBanners();

    this.init = function() {
        this.refresh(bannerInIdx, 100);
    };

    this.drawCanvasRect = function() {
        this.ctx.save();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = strokeColor[strokeIdx];
        this.ctx.fillStyle = canvasColor;
        this.ctx.lineWidth = 2;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.restore();
    };

    this.refresh = function(idx, opacity) {
        this.ctx.save();
        this.ctx.canvas.width = document.body.offsetWidth/2;
        this.ctx.canvas.height = document.body.offsetHeight/4;

        this.drawCanvasRect();

        this.aBanners = [];
        this.aBanners.push(new Picture(padding, padding, document.body.offsetWidth/2 - (padding*2), document.body.offsetHeight/4 - (padding*2), this.banners.banner, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.logo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.redLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.blueLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.greenLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.yellowLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.orangeLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.cyanLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.purpleLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.pinkLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.whiteLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.greyLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.blackLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.brownLogo, this.canvas));
        this.aBanners.push(new Picture(0, 0, this.ctx.canvas.width, this.ctx.canvas.height, this.banners.notFound, this.canvas));

        this.ctx.globalAlpha = opacity;
        this.aBanners[idx].draw();

        this.ctx.restore();
    };

    this.simpleDraw = function(idx, opacity) {
        this.ctx.save();
        this.ctx.globalAlpha = opacity;
        this.aBanners[idx].draw();
        this.ctx.restore();
    };
}

/** Função complementar ao objeto SearchX que serve para o carregamento das imagens dos Banners e Logos *
 *
 * @constructor
 */
function AppBanners() {
    this.banner = new Image();
    this.logo = new Image();
    this.redLogo = new Image();
    this.blueLogo = new Image();
    this.greenLogo = new Image();
    this.yellowLogo = new Image();
    this.orangeLogo = new Image();
    this.cyanLogo = new Image();
    this.purpleLogo = new Image();
    this.pinkLogo = new Image();
    this.whiteLogo = new Image();
    this.greyLogo = new Image();
    this.blackLogo = new Image();
    this.brownLogo = new Image();
    this.notFound = new Image();

    var numImages = 14;
    var numLoaded = 0;

    function imageLoaded() {
        numLoaded++;
        if(numLoaded === numImages) {
            app.init();
        }
    }

    this.banner.onload = function() {
        imageLoaded();
    };

    this.logo.onload = function() {
        imageLoaded();
    };

    this.redLogo.onload = function() {
        imageLoaded();
    };

    this.blueLogo.onload = function() {
        imageLoaded();
    };

    this.greenLogo.onload = function() {
        imageLoaded();
    };

    this.yellowLogo.onload = function() {
        imageLoaded();
    };

    this.orangeLogo.onload = function() {
        imageLoaded();
    };

    this.cyanLogo.onload = function() {
        imageLoaded();
    };

    this.purpleLogo.onload = function() {
        imageLoaded();
    };

    this.pinkLogo.onload = function() {
        imageLoaded();
    };

    this.whiteLogo.onload = function() {
        imageLoaded();
    };

    this.greyLogo.onload = function() {
        imageLoaded();
    };

    this.blackLogo.onload = function() {
        imageLoaded();
    };

    this.brownLogo.onload = function() {
        imageLoaded();
    };

    this.notFound.onload = function() {
        imageLoaded();
    };

    this.banner.src = "images/logos/Banner.jpg";
    this.logo.src = "images/logos/logo.png";
    this.redLogo.src = "images/logos/logo_red.png";
    this.blueLogo.src = "images/logos/logo_blue.png";
    this.greenLogo.src = "images/logos/logo_green.png";
    this.yellowLogo.src = "images/logos/logo_yellow.png";
    this.orangeLogo.src = "images/logos/logo_orange.png";
    this.cyanLogo.src = "images/logos/logo_cyan.png";
    this.purpleLogo.src = "images/logos/logo_purple.png";
    this.pinkLogo.src = "images/logos/logo_pink.png";
    this.whiteLogo.src = "images/logos/logo_white.png";
    this.greyLogo.src = "images/logos/logo_grey.png";
    this.blackLogo.src = "images/logos/logo_black.png";
    this.brownLogo.src = "images/logos/logo_brown.png";
    this.notFound.src = "images/logos/404.png";
}

/** Objeto que representa uma Imagem, sendo utilizado em todas as imagens da aplicação multimédia representadas no canvas *
 *
 * @param x
 * @param y
 * @param w
 * @param h
 * @param img
 * @param canvas
 * @constructor
 */
function Picture(x, y, w, h, img, canvas) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.img = img;
    this.ctx = canvas.getContext("2d");

    this.draw = function() {
        this.ctx.drawImage(this.img, this.x, this.y, this.w, this.h);
    };

    this.overcheck = function (mx,my) {
        if ( (mx>=this.x)&&(mx<=(this.x+this.w))&&(my>=this.y)&&(my<=(this.y+this.h))) {
            return true;
        }
        return false;
    };

}
Picture.prototype = Object.create(Picture.prototype);
Picture.prototype.constructor = Picture;

/** Função que define a cor do canvas, consoante o tipo de banner que se encontra ativo, na página principal *
 *
 * @param color
 * @param canvas
 */
function setCnvsColor(color, canvas) {
    if(fadePerc > 0) {
        return;
    }
    searchColor = color;

    switch(bannerInIdx) {
        case 0:
            canvasColor = color;
            document.getElementById(canvas).style.backgroundColor = color;
            app.refresh(bannerInIdx, 100);
            break;
        default :
            canvasColor = 'transparent';
            document.getElementById(canvas).style.backgroundColor = 'transparent';
            switch(color) {
                case 'transparent':
                    bannerOutIdx = 1;
                    break;
                case '#c43c35':
                    bannerOutIdx = 2;
                    break;
                case '#269CE9':
                    bannerOutIdx = 3;
                    break;
                case '#57a957':
                    bannerOutIdx = 4;
                    break;
                case '#ffde00':
                    bannerOutIdx = 5;
                    break;
                case '#ffA500':
                    bannerOutIdx = 6;
                    break;
                case '#20b2aa':
                    bannerOutIdx = 7;
                    break;
                case '#800080':
                    bannerOutIdx = 8;
                    break;
                case '#ffb6c1':
                    bannerOutIdx = 9;
                    break;
                case '#ffffff':
                    bannerOutIdx = 10;
                    break;
                case '#888888':
                    bannerOutIdx = 11;
                    break;
                case '#000000':
                    bannerOutIdx = 12;
                    break;
                case '#8b4513':
                    bannerOutIdx = 13;
                    break;
            }
            setNextBanner();
            break;
    }
}

/** Função que efetua a alteração do banner 1 para o banner 2 */
function switchLogo() {
    if(fadePerc > 0) {
        return;
    }
    if(bannerInIdx == 0) {
        setCnvsColor('transparent', 'canvas');
    }
    if(bannerInIdx >= 1 & bannerOutIdx >= 1) {
        bannerOutIdx = 0;
    }
    setNextBanner();
}

/** Função responsável pela animação de fade entre as diferentes imagens no canvas */
function setNextBanner() {
    if(bannerOutIdx > 1) {
        strokeIdx = 1;
    } else {
        strokeIdx = bannerOutIdx;
    }
    if (fadePerc > 100) {
        fadePerc = 0;
        var oldInIdx = bannerInIdx;
        bannerInIdx = bannerOutIdx;
        if(oldInIdx > 1) {
            bannerOutIdx = 1;
        } else {
            bannerOutIdx = oldInIdx;
        }
        return;
    }

    requestAnimationFrame(setNextBanner);
    app.drawCanvasRect();
    app.simpleDraw(bannerOutIdx, (fadePerc / 100));
    app.simpleDraw(bannerInIdx, (1 - (fadePerc / 100)));
    fadePerc++;
}
/** */

/** Funções complementares que servem de conversão entre as cores em formato rgb e as cores em hexadecimal *
 *
 * @param hexColor
 * @returns {*[]}
 */
function hex2Rgb(hexColor) {
    if (hexColor.lastIndexOf('#') > -1) {
        hexColor = hexColor.replace(/#/, '0x');
    } else {
        hexColor = '0x' + hexColor;
    }
    var redColor   = (hexColor >> 16) & 0xFF;
    var greenColor = (hexColor >> 8) & 0xFF;
    var blueColor  = hexColor & 0xFF;
    return [redColor, greenColor, blueColor];
}

function rgb2Hex(rgbColor){
    rgbColor = rgbColor.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    return (rgbColor && rgbColor.length === 4) ? "#" +
    ("0" + parseInt(rgbColor[1],10).toString(16)).slice(-2) +
    ("0" + parseInt(rgbColor[2],10).toString(16)).slice(-2) +
    ("0" + parseInt(rgbColor[3],10).toString(16)).slice(-2) : '';
}
/** */

/** Funções que controlam a visualização dos resultados da pesquisa */

/** Objeto Search que representa uma pesquisa de conteúdo multimédia  *
 *
 * @param stringSearch
 * @constructor
 */
function Search(stringSearch) {
    if(stringSearch != "") {
        var xml = new XML_Data("xml/My_database.xml", stringSearch);
        xml.init();

        if (xml.searched.length > 0) {
            xml.buildLS();
            window.location.href = 'searchWithCanvas.html';
        } else {
            if(window.location.href.split('/').pop() == 'index.html') {
                bannerOutIdx = 14;
                setNextBanner();
                setTimeout(function() {setNextBanner()}, 7000);
            } else {
                window.location.href = 'noresult.html';
            }

        }
    }
}

/** Handler do evento que controla a pesquisa por tecla Enter *
 *
 * @param stringSearch
 */
function enterSearch(ev, stringSearch) {
    if(ev.keyCode == 13) {
        Search(stringSearch);
    }
    return false;
}

/** Objeto que representa o ficheiro XML de resposta em memória e as respetivas funções de manipulação da base de dados em XML *
 *
 * @param file
 * @param stringSearch
 * @constructor
 */
function XML_Data(file, stringSearch) {
    this.filename = file;
    var localStorageName = "SearchX";
    var xmlRowString = "<ImageStorage>";
    var searchWord = stringSearch.toLowerCase();
    this.images = [];
    this.searched = [];
    var sColor,
        path = "",
        title = "",
        dColor = "",
        colorOffset = 110;

    this.init = function() {
        this.readXML();
    };

    this.readXML = function() {
        sColor = hex2Rgb(searchColor);                                                              // Converter a cor de pesquisa para o formato RGB em Array

        var xmlDoc = this.loadXML();
        this.images = xmlDoc.getElementsByTagName("image");
        for(var i = 0; i < this.images.length; i++) {
            if(this.images[i].getElementsByTagName("title")[0].hasChildNodes()) {
                var t = this.images[i].getElementsByTagName("title")[0].childNodes[0].nodeValue.toLowerCase().search(searchWord);
                var c = this.images[i].className.search(searchWord);
                if(t >= 0 | c >= 0 | searchWord == "") {

                    /** Filtrar cores antes de adicionar ao LS */
                    /** Obter cor do XML - Mais tarde poderá ser substituida pela cor dominante do LS referente à imagem em questão*/
                    dColor = this.images[i].getElementsByTagName("dominantcolor")[0].childNodes[0].nodeValue;   // Obter a cor dominante do XML
                    dColor = hex2Rgb(dColor);                                                                   // Converter a cor em hexa para o formato RGB em Array
                    if ((dColor[0] > (sColor[0] - colorOffset) & dColor[0] < (sColor[0] + colorOffset)) & (dColor[1] > (sColor[1] - colorOffset) & dColor[1] < (sColor[1] + colorOffset)) & (dColor[2] > (sColor[2] - colorOffset) & dColor[2] < (sColor[2] + colorOffset))) {
                        this.searched.push(this.images[i]);
                    } else if((searchColor == 'transparent')) {
                        this.searched.push(this.images[i]);
                    }
                    /**  */
                }
            }
        }
    };

    this.loadXML = function() {
        var xmlhttp;
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
        }
        xmlhttp.open("GET", this.filename, false);
        xmlhttp.send();
        return xmlhttp.responseXML;
    };

    this.buildLS = function() {
        xmlRowString += "<" + searchWord + ">";

        for(var i = 0; i < this.searched.length; i++) {
            xmlRowString += "<images>";
            xmlRowString += "<path>" + this.searched[i].getElementsByTagName("path")[0].childNodes[0].nodeValue + "</path>";
            xmlRowString += "</images>";
        }

        xmlRowString += "</" + searchWord + "></ImageStorage>";

        if (typeof(localStorage) == 'undefined')
            alert('Your browser does not support HTML5 localStorage. Try upgrading.');
        else {
            try {
                localStorage.setItem(localStorageName, xmlRowString);
            }
            catch (e) {
                alert("save failed!");
            }
        }
    };
}

/** Funções que representam a aplicação multimédia na vertente de resultados */
/** Função que obtém os resultados na página de resultados com canvas *
 *
 * @constructor
 */
function ResultsWithCanvas() {

    this.localStorageRow = window.localStorage.getItem("SearchX");
    this.parser = new DOMParser();
    this.xmlDoc = this.parser.parseFromString(this.localStorageRow, "text/html");
    results = this.xmlDoc.getElementsByTagName("images");

    if(results.length >= maxResults) {
        total_results = maxResults;
    } else {
        total_results = results.length;
    }

    this.init = function() {
        this.x = padding;
        this.y = padding;
        this.w = document.body.offsetWidth/cols - padding;
        this.h = document.body.offsetHeight/rows - padding;
        this.idx = 0;
        this.imageLoaded = 0;
        Images = [];
        canvas2Resize();
    };


    this.loadResults = function() {
        this.canvas = document.getElementById("canvas2");
        this.ctx = this.canvas.getContext("2d");
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.idx = 0;

        for(var i = 0; i < total_results; i++) {
            this.img = new Image();

            this.img.onload = function () {
                resultPage.ImageLoaded();
            };

            this.img.src = results[this.idx++].childNodes[0].childNodes[0].nodeValue;

            var pic = new Picture(this.x, this.y, this.w, this.h, this.img, document.getElementById("canvas2"));

            Images.push(pic);

            if((this.x + document.body.offsetWidth/cols + padding) > document.body.offsetWidth) {
                this.x = padding;
                this.y += document.body.offsetHeight/rows + padding;
            } else {
                this.x += document.body.offsetWidth/cols + padding;
            }
        }
    };

    this.ImageLoaded = function() {
        this.imageLoaded++;
        if(this.imageLoaded == total_results) {
            this.drawResultsWithCanvas();
        }
    };

    this.drawResultsWithCanvas = function() {
        for(var i = 0; i < Images.length; i++) {
            Images[i].draw();
        }
    }
}

/** Função que controla o resize do canvas da página de resultados */
function canvas2Resize() {
    var canvas = document.getElementById("canvas2");
    var ctx = canvas.getContext("2d");
    ctx.canvas.width = document.body.offsetWidth;
    var height = Math.ceil((total_results/cols)) * Math.ceil((document.body.offsetHeight/rows + padding));
    if(height < document.body.offsetHeight)
        ctx.canvas.height = document.body.offsetHeight;
    else
        ctx.canvas.height = height;
}

/** Iniciar uma nova página de resultados */
function initSearchResultPageWithCanvas() {
    window.addEventListener('resize', loadImagesFromResultsWithCanvas, false);
    window.addEventListener('click', loadImage, false);
    window.addEventListener('mousemove', mouseOver, false);
    resultPage = new ResultsWithCanvas();
    loadImagesFromResultsWithCanvas();
}

/** CRiação de uma nova página de resultados */
function loadImagesFromResultsWithCanvas() {
    resultPage.init();
    resultPage.loadResults();

}

/** Função que define a cor do header da página de resultados *
 *
 * @param color
 */
function setHeaderColor(color) {
    searchColor = color;
    document.getElementById("searchBar").style.backgroundColor = searchColor;
    if(searchColor == "transparent") {
        document.getElementById("logo").src = "images/logos/searchx.png"
    } else {
        document.getElementById("logo").src = "images/logos/searchx_black.png"
    }
}

/** Funções complementares que controlam os eventos no canvas da página de resultados */
/** Abrir a imagem na resolução original *
 *
 * @param ev
 */
function loadImage(ev) {
    var canvas = document.getElementById("canvas2");
    var rect = canvas.getBoundingClientRect();
    var mx = ev.clientX - rect.left;
    var my = ev.clientY - rect.top;

    /** Função para correr todas as imagens no mouseOver */
    Images.forEach(function(pic) {
        if(pic.overcheck(mx, my)) {
            window.location.href = pic.img.src;
        }
    });
}

/** Alterar o ícon do rato quando em cima de uma imagem *
 *
 * @param ev
 */
function mouseOver(ev) {
    var canvas = document.getElementById("canvas2");
    canvas.style.cursor = "auto";
    var rect = canvas.getBoundingClientRect();
    var mx = ev.clientX - rect.left;
    var my = ev.clientY - rect.top;

    /** Função para correr todas as imagens no mouseOver */
    Images.forEach(function(pic) {
         if(pic.overcheck(mx, my)) {
             canvas.style.cursor = "pointer";
         }
    });
}

/** OLD - Função utilizada com HTML dinâmico sem Canvas*/
function Results() {
    this.localStorageRow = window.localStorage.getItem("SearchX");
    this.parser = new DOMParser();
    this.xmlDoc = this.parser.parseFromString(this.localStorageRow, "text/html");
    this.results = this.xmlDoc.getElementsByTagName("images");

    this.loadResults = function() {
        this.path = null;
        this.idx = 0;

        for(var r = 0; (r * cols) < this.results.length & r < rows; r++) {
            this.div = document.createElement('div');
            this.div.className = 'row';

            for(var c = 0; c < this.results.length & c < cols; c++) {
                this.path = this.results[this.idx++].childNodes[0].childNodes[0].nodeValue;
                this.img = new Image();
                this.img.src = this.path;
                this.img.onmouseover = function() { this.style.cursor = "pointer"};
                this.img.onclick = function() { window.location.href = this.src };
                this.div.appendChild(this.img);
            }
            document.getElementById("search").appendChild(this.div);
        }
    };
}

/** OLD - Função utilizada com HTML dinâmico sem Canvas*/
function loadImagesFromResults() {
    resultPage = new Results();
    resultPage.loadResults();
}