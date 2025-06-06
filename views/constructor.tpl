% rebase('layout.tpl', title='PC Builder', year=year)

<link rel="stylesheet" href="/static/content/page_styles/styles_constructor.css">

<div class="jumbotron constructor-header">
    <div class="constructor-header-text">
        <h1>PC Assembly</h1>
        <p class="lead">Create your ideal computer by choosing from the best components!</p>
        <button onclick="showAdvice()" class="btn-advice">
            Get Advice
        </button>
    </div>
    <img src="/static/resources/logo.png" alt="Constructor Logo" class="constructor-logo">
</div>

<script>
    function showAdvice() {
        alert("Choose components that are compatible with each other and fit your needs for performance and budget!");
    }
</script>

<div class="row">
    <div class="col-md-4">
        <h2>Processors</h2>
        <p>Choose a powerful processor that meets your needs. We offer a wide selection from Intel and AMD.</p>
        <select class="form-control" id="cpu-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Processor</option>
            <option value="intel_i5" data-price="11500">Intel Core i5</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Motherboards</h2>
        <p>Find the perfect motherboard for your processor and other components.</p>
        <select class="form-control" id="motherboard-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Motherboard</option>
            <option value="asus_rog" data-price="3500">ASUS ROG Strix</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Graphics Cards</h2>
        <p>Choose a graphics card for gaming and professional graphics to achieve maximum performance.</p>
        <select class="form-control" id="gpu-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Graphics Card</option>
            <option value="nvidia_gtx_1660" data-price="9750">NVIDIA GTX 1660</option>
        </select>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>RAM</h2>
        <p>Add RAM to ensure high-speed performance for your computer.</p>
        <select class="form-control" id="ram-select" onchange="selectComponent()">
            <option value="" data-price="0">Select RAM</option>
            <option value="8gb_ddr4" data-price="1250">8GB DDR4</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Storage</h2>
        <p>Select SSD or HDD for storing your data and applications.</p>
        <select class="form-control" id="storage-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Storage</option>
            <option value="ssd_256gb" data-price="6100">SSD 256GB</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Cases</h2>
        <p>Choose a case for your PC to ensure good ventilation and a stylish appearance.</p>
        <select class="form-control" id="case-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Case</option>
            <option value="mid_tower" data-price="5400">Mid Tower</option>
        </select>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>Power Supply</h2>
        <p>Select a suitable power supply that provides enough power for its components.</p>
        <select class="form-control" id="power-supply-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Power Supply</option>
            <option value="KSAS" data-price="1500">KSAS BOOM</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Coolers</h2>
        <p>Select a cooler to prevent overheating of the processor and other components in the computer.</p>
        <select class="form-control" id="cooler-select" onchange="selectComponent()">
            <option value="" data-price="0">Select Cooler</option>
            <option value="aerocool" data-price="670">AeroCool MegaFreeze</option>
        </select>
    </div>
</div>

<div class="jumbotron total-cost-block">
    <div class="text-center">
        <div class="total-cost-box"> 
            <h3 id="total-cost">Total PC cost: 0.00 rub</h3>
        </div>
        <p>
            <a href="#payment" class="btn-payment">
                Proceed to Payment
                <img src="/static/resources/buy_logo.png" alt="Constructor Logo" class="buy-logo">
            </a>
        </p>
    </div>
</div>

<script>
function selectComponent() {
    const components = [
        'cpu-select',
        'motherboard-select',
        'gpu-select',
        'ram-select',
        'storage-select',
        'case-select',
        'power-supply-select',
        'cooler-select'
    ];
    
    let totalCostKopecks = 0;

    components.forEach(component => {
        const selectElement = document.getElementById(component);
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        const price = parseInt(selectedOption.getAttribute('data-price')) || 0;
        totalCostKopecks += price;
    });

    const totalCostRub = Math.floor(totalCostKopecks);
    const totalCostKopecksDisplay = (totalCostKopecks % 1 * 100).toFixed(0);
    document.getElementById('total-cost').innerText = `Total PC cost: ${totalCostRub}.${totalCostKopecksDisplay.padStart(2, '0')} rub`;
}
</script>