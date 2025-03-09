% rebase('layout.tpl', title='PC Builder', year=year)

<div class="jumbotron" style="background-color: orange; color: white;">
    <h1>Сборка ПК</h1>
    <p class="lead">Создайте свой идеальный компьютер, выбирая из лучших комплектующих.</p>
    <p><a href="#payment" class="btn btn-primary btn-large">Перейти к оплате</a></p>
    <p><a href="/home" class="btn btn-primary btn large">Перейти в каталог</a></p>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>Процессоры</h2>
        <p>Выберите мощный процессор, который соответствует вашим потребностям. Мы предлагаем широкий выбор от Intel и AMD.</p>
        <select class="form-control" id="cpu-select">
            <option value="">Выберите процессор</option>
            <option value="intel_i5">Intel Core i5</option>
            <option value="intel_i7">Intel Core i7</option>
            <option value="amd_ryzen_5">AMD Ryzen 5</option>
            <option value="amd_ryzen_7">AMD Ryzen 7</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Материнские платы</h2>
        <p>Найдите идеальную материнскую плату для вашего процессора и других комплектующих.</p>
        <select class="form-control" id="motherboard-select">
            <option value="">Выберите материнскую плату</option>
            <option value="asus_rog">ASUS ROG Strix</option>
            <option value="msi_b450">MSI B450</option>
            <option value="gigabyte_b550">Gigabyte B550</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Видеокарты</h2>
        <p>Выберите видеокарту для игр и профессиональной графики, чтобы получить максимальную производительность.</p>
        <select class="form-control" id="gpu-select">
            <option value="">Выберите видеокарту</option>
            <option value="nvidia_gtx_1660">NVIDIA GTX 1660</option>
            <option value="nvidia_rtx_3060">NVIDIA RTX 3060</option>
            <option value="amd_rx_6700">AMD RX 6700</option>
        </select>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>Оперативная память</h2>
        <p>Добавьте оперативную память для обеспечения высокой скорости работы вашего компьютера.</p>
        <select class="form-control" id="ram-select">
            <option value="">Выберите оперативную память</option>
            <option value="8gb_ddr4">8GB DDR4</option>
            <option value="16gb_ddr4">16GB DDR4</option>
            <option value="32gb_ddr4">32GB DDR4</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Накопители</h2>
        <p>Выберите SSD или HDD для хранения ваших данных и приложений.</p>
        <select class="form-control" id="storage-select">
            <option value="">Выберите накопитель</option>
            <option value="ssd_256gb">SSD 256GB</option>
            <option value="ssd_512gb">SSD 512GB</option>
            <option value="hdd_1tb">HDD 1
        </select>
    </div>
    <div class="col-md-4">
        <h2>Корпуса</h2>
        <p>Выберите корпус для вашего ПК, чтобы обеспечить хорошую вентиляцию и стильный внешний вид.</p>
        <select class="form-control" id="case-select">
            <option value="">Выберите корпус</option>
            <option value="mid_tower">Mid Tower</option>
            <option value="full_tower">Full Tower</option>
            <option value="mini_tower">Mini Tower</option>
        </select>
    </div>
</div>

<script>
function selectComponent(selectId) {
    const selectedOption = document.getElementById(selectId).value;
    if (selectedOption) {
        alert('Вы выбрали: ' + selectedOption);
        // Заглушка для будущей реализации
    } else {
        alert('Пожалуйста, выберите компонент.');
    }
}
</script>