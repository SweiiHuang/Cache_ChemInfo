//homepage
let currentLocation = window.location.origin
let backHomepage = document.querySelector(".menu-title")
backHomepage.setAttribute("href", currentLocation)


const downloadBtn = document.querySelector('.download-pdf');
const content = document.querySelector('.photo-grid-item');

downloadBtn.addEventListener('click', () => {

    const options = {
        margin: [1, 0, 1, 0], // 設定 margin 為 0，下載的內容填滿頁面
        filename: 'downloaded.pdf', //下載檔名
        image: { type: 'png', quality: 1 }, // 設定圖片格式和品質
        pagebreak: ['css', 'avoid'], //避免分頁
        html2canvas: { scale: 3 }, // 設定 html2canvas 比例
        jsPDF: { unit: 'mm', format: 'a3', orientation: 'portrait' } // 下載的文件格式
    };


    // 執行 html2pdf 函式，將 content 內容下載為 PDF
    html2pdf().set(options).from(content).save();

    // 下載完畢後，將 content 的高度改回 300px


});

// search results
const getResult = document.querySelector(".header-main-search-img")
const keyInResult = document.querySelector(".header-main-search-input")
getResult.addEventListener("click", handleInputEvent)
keyInResult.addEventListener("keydown", handleInputEvent)


function handleInputEvent(event) {
    if (event.type === "click" || (event.type === "keydown" && event.key === "Enter")) {
        // clear tbody-box previous result
        refreshInfo();
        // let tbodyBox = document.querySelector(".tbody-box");
        // while (tbodyBox.firstChild) {
        //     tbodyBox.removeChild(tbodyBox.firstChild);
        // }

        // let tbodyBoxGlobal = document.querySelector(".tbody-box-global");
        // while (tbodyBoxGlobal.firstChild) {
        //     tbodyBoxGlobal.removeChild(tbodyBoxGlobal.firstChild);
        // }

        // const showData = document.querySelector(".photo-grid-item")
        // showData.style.display = "block"

        const keyword = document.querySelector(".header-main-search-input").value;

        getPropertyInfo(keyword);
        getCustomsInfo(keyword);
        getInventoryInfo(keyword);

    }
}

const example = document.querySelector(".search-eg1")
example.addEventListener('click', () => {
    refreshInfo();
    getPropertyInfo("100-97-0");
    getCustomsInfo("100-97-0");
    getInventoryInfo("100-97-0");

})

function refreshInfo() {
    // clear tbody-box previous result
    let tbodyBox = document.querySelector(".tbody-box");
    while (tbodyBox.firstChild) {
        tbodyBox.removeChild(tbodyBox.firstChild);
    }

    let tbodyBoxGlobal = document.querySelector(".tbody-box-global");
    while (tbodyBoxGlobal.firstChild) {
        tbodyBoxGlobal.removeChild(tbodyBoxGlobal.firstChild);
    }

    const showData = document.querySelector(".photo-grid-item")
    showData.style.display = "block"

    const showDownload =
        document.querySelector(".download-pdf")
    showDownload.style.display = "block"
}
// getResult.addEventListener("click", () => {
//     // clear tbody-box previous result
//     let tbodyBox = document.querySelector(".tbody-box");
//     while (tbodyBox.firstChild) {
//         tbodyBox.removeChild(tbodyBox.firstChild);
//     }

//     let tbodyBoxGlobal = document.querySelector(".tbody-box-global");
//     while (tbodyBoxGlobal.firstChild) {
//         tbodyBoxGlobal.removeChild(tbodyBoxGlobal.firstChild);
//     }

//     const showData = document.querySelector(".photo-grid-item")
//     showData.style.display = "block"

//     const keyword = document.querySelector(".header-main-search-input").value;

//     getPropertyInfo(keyword);
//     getCustomsInfo(keyword);
//     getInventoryInfo(keyword);

// });


function getPropertyInfo(keyword) {
    fetch(`/api/ChemPropertyList/?cas_no=${keyword}`)
        .then(response => response.json())
        .then(({ results: [{ cas_no: cas, image: svg, name, molecular_formula: formula, molecular_mass: mass, boiling_point: boil, melting_point: melt, density }] }) => {
            document.querySelector(".property-pic-cas").textContent = cas;
            document.querySelector(".property-pic-svg").innerHTML = svg;
            document.querySelector(".property-pic-name").textContent = name;
            document.querySelector(".property-text-formula").innerHTML = formula;
            document.querySelector(".property-text-mass").textContent = mass;
            document.querySelector(".property-text-boil").textContent = boil;
            document.querySelector(".property-text-melt").textContent = melt;
            document.querySelector(".property-text-density").innerHTML = density;
        });
}

function getCustomsInfo(keyword) {
    fetch(`/api/ChemIdList/?cas_rn=${keyword}`)
        .then(response => response.json())
        .then(({ results }) => {

            const row = document.querySelector(".tbody-box");

            if (results.length === 0) {
                row.textContent = "No information, please check again";
            } else {
                results.forEach(({ name, cas_rn, cn_code, ec_number, un_number }) => {
                    const hsCode = cn_code.substring(0, 6);

                    const row0 = document.createElement("tr");
                    row0.style = "tr-row"
                    row.appendChild(row0);

                    const row1 = document.createElement("th");
                    const row2 = document.createElement("td");
                    const row3 = document.createElement("td");
                    const row4 = document.createElement("td");
                    const row5 = document.createElement("td");
                    row1.style.scope = "row";
                    row1.textContent = name;
                    row2.textContent = cas_rn;
                    row3.textContent = hsCode;
                    row4.textContent = ec_number;
                    row5.textContent = un_number;
                    row0.appendChild(row1)
                    row0.appendChild(row2)
                    row0.appendChild(row3)
                    row0.appendChild(row4)
                    row0.appendChild(row5)
                });
            }
        });
}

function getInventoryInfo(keyword) {
    fetch(`/api/CheckData/?cas_no=${keyword}`)
        .then(response => response.json())
        .then(data => {
            const row = document.querySelector(".tbody-box-global");


            const results = [
                { region: "Taiwan", name: "Concerned Chemical Substances", data: data.concern_data },
                { region: "Taiwan", name: "Controlled Chemicals", data: data.control_data },
                { region: "Taiwan", name: "Priority Management Chemicals", data: data.priority_data },
                { region: "Taiwan", name: "Toxic Chemical Substances", data: data.toxic_data },
            ];
            // console.log(results);

            for (const result of results) {
                const row0 = document.createElement("tr");
                row0.style = "tr-row";
                row.appendChild(row0);


                const invRegion = document.createElement("th");
                const invName = document.createElement("td");
                const invListed = document.createElement("td");
                const invCas = document.createElement("td");
                const invEnName = document.createElement("td");
                const invCnName = document.createElement("td");

                if (result.data !== null) {
                    invRegion.textContent = result.region;
                    invName.textContent = result.name;
                    invListed.textContent = "Yes";
                    invCas.textContent = result.data.cas_no;
                    invEnName.textContent = result.data.en_name;
                    invCnName.textContent = result.data.cn_name;
                } else {
                    invRegion.textContent = result.region;
                    invName.textContent = result.name;
                    invListed.textContent = "No";
                    invCas.textContent = "-";
                    invEnName.textContent = "-";
                    invCnName.textContent = "-";
                }

                row0.appendChild(invRegion);
                row0.appendChild(invName);
                row0.appendChild(invListed);
                row0.appendChild(invCas);
                row0.appendChild(invEnName);
                row0.appendChild(invCnName);
            }
        })
        .catch(error => console.error(error));
}



//Close Result
const clickHide = document.querySelector(".photo-grid-close-btn ")
clickHide.addEventListener("click", function () {
    let hideData = document.querySelector(".photo-grid-item")
    hideData.style.display = "none";

    let searchInput = document.querySelector(".header-main-search-input");
    searchInput.value = '';


    document.querySelector(".download-pdf").style.display = "none"

    location.reload()
})