% rebase('layout.tpl', title='PC Builder', year=year)

<div class="jumbotron" style="background-color: orange; color: white; margin-top: 20px; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
    <div style="margin-left: 20px;">
        <h1>PC Assembly</h1>
        <p class="lead">Create your ideal computer by choosing from the best components!</p>
    </div>
    <img src="/static/resources/logo.png" alt="Constructor Logo" style="max-width: 200px; height: auto; margin-left: 20px;">
</div>

<div class="row">
    <div class="col-md-4">
        <h2>Processors</h2>
        <p>Choose a powerful processor that meets your needs. We offer a wide selection from Intel and AMD.</p>
        <select class="form-control" id="cpu-select" onchange="selectComponent('cpu-select')">
            <option value="">Select Processor</option>
            <option value="intel_i5">Intel Core i5</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Motherboards</h2>
        <p>Find the perfect motherboard for your processor and other components.</p>
        <select class="form-control" id="motherboard-select" onchange="selectComponent('motherboard-select')">
            <option value="">Select Motherboard</option>
            <option value="asus_rog">ASUS ROG Strix</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Graphics Cards</h2>
        <p>Choose a graphics card for gaming and professional graphics to achieve maximum performance.</p>
        <select class="form-control" id="gpu-select" onchange="selectComponent('gpu-select')">
            <option value="">Select Graphics Card</option>
            <option value="nvidia_gtx_1660">NVIDIA GTX 1660</option>
        </select>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>RAM</h2>
        <p>Add RAM to ensure high-speed performance for your computer.</p>
        <select class="form-control" id="ram-select" onchange="selectComponent('ram-select')">
            <option value="">Select RAM</option>
            <option value="8gb_ddr4">8GB DDR4</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Storage</h2>
        <p>Select SSD or HDD for storing your data and applications.</p>
        <select class="form-control" id="storage-select" onchange="selectComponent('storage-select')">
            <option value="">Select Storage</option>
            <option value="ssd_256gb">SSD 256GB</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Cases</h2>
        <p>Choose a case for your PC to ensure good ventilation and a stylish appearance.</p>
        <select class="form-control" id="case-select" onchange="selectComponent('case-select')">
            <option value="">Select Case</option>
            <option value="mid_tower">Mid Tower</option>
        </select>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>Power Supply</h2>
        <p>Select a suitable power supply that provides enough power for its components.</p>
        <select class="form-control" id="power-supply-select" onchange="selectComponent('power-supply-select')">
            <option value="">Select Power Supply</option>
            <option value="KSAS">KSAS BOOM</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Coolers</h2>
        <p>Select a cooler to prevent overheating of the processor and other components in the computer.</p>
        <select class="form-control" id="cooler-select" onchange="selectComponent('cooler-select')">
            <option value="">Select Cooler</option>
            <option value="aerocool">AeroCool MegaFreeze</option>
        </select>
    </div>
</div>

<div class="d-flex align-items-center justify-content-center jumbotron" style="background-color: orange; color: white; margin-top: 40px; padding: 20px;">
    <div class="text-center">
        <div style="background-color: #ffcc80; border-radius: 15px; padding: 20px; display: inline-block;"> 
            <h2 style="margin: 0;">Total PC cost: 10000 rub</h2>
        </div>
        <p>
            <a href="#payment" class="btn btn-large btn-lg" style="background-color: #fdf5e6; color: #333; margin-top: 20px;">Proceed to Payment</a>
        </p>
    </div>
</div>

<script>
function selectComponent(selectId) {
    const selectedOption = document.getElementById(selectId).value;
    if (selectedOption) {
        alert('You selected: ' + selectedOption);
        // Placeholder for future implementation
    } else {
        alert('Please select a component.');
    }
}
</script>
