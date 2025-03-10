% rebase('layout.tpl', title='PC Builder', year=year)

<div class="jumbotron" style="background-color: orange; color: white; margin-top: 20px; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
    <div style="margin-left: 20px;">
        <h1>Сборка ПК</h1>
        <p class="lead">Создайте свой идеальный компьютер, выбирая из лучших комплектующих!</p>
    </div>
    <img src="/static/resources/logo.png" alt="Constructor Logo" style="max-width: 200px; height: auto; margin-left: 20px;">
</div>



<div class="row">
    <div class="col-md-4">
        <h2>Процессоры</h2>
        <p>Выберите мощный процессор, который соответствует вашим потребностям. Мы предлагаем широкий выбор от Intel и AMD.</p>
        <select class="form-control" id="cpu-select">
            <option value="">Выберите процессор</option>
            <option value="intel_i5">Intel Core i5</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Материнские платы</h2>
        <p>Найдите идеальную материнскую плату для вашего процессора и других комплектующих.</p>
        <select class="form-control" id="motherboard-select">
            <option value="">Выберите материнскую плату</option>
            <option value="asus_rog">ASUS ROG Strix</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Видеокарты</h2>
        <p>Выберите видеокарту для игр и профессиональной графики, чтобы получить максимальную производительность.</p>
        <select class="form-control" id="gpu-select">
            <option value="">Выберите видеокарту</option>
            <option value="nvidia_gtx_1660">NVIDIA GTX 1660</option>
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
        </select>
    </div>
    <div class="col-md-4">
        <h2>Накопители</h2>
        <p>Выберите SSD или HDD для хранения ваших данных и приложений.</p>
        <select class="form-control" id="storage-select">
            <option value="">Выберите накопитель</option>
            <option value="ssd_256gb">SSD 256GB</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Корпуса</h2>
        <p>Выберите корпус для вашего ПК, чтобы обеспечить хорошую вентиляцию и стильный внешний вид.</p>
        <select class="form-control" id="case-select">
            <option value="">Выберите корпус</option>
            <option value="mid_tower">Mid Tower</option>
        </select>
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h2>Блок питания</h2>
        <p>Выберите себе подходящий блок питания, который обеспечит достаточную подачу питания на его компоненты.</p>
        <select class="form-control" id="ram-select">
            <option value="">Выберите блок питания</option>
            <option value="KSAS">KSAS BOOM</option>
        </select>
    </div>
    <div class="col-md-4">
        <h2>Кулер</h2>
        <p>Выберите кулер, чтобы не допустить перегрева процессора и воздуха в компьютере.</p>
        <select class="form-control" id="storage-select">
            <option value="">Выберите кулер</option>
            <option value="aerocool">AeroCool MegaFreeze</option>

        </select>
    </div>
</div>

    <div class="d-flex align-items-center justify-content-center jumbotron" style="background-color: orange; color: white; margin-top: 40px; padding: 20px;">
        <div class="text-center">
            <div style="background-color: #ffcc80; border-radius: 15px; padding: 20px; display: inline-block;"> 
                <h2 style="margin: 0;">Сумма сборки ПК: ???</h2>
            </div>
            <p>
                <a href="#payment" class="btn btn-large btn-lg" style="background-color: #fdf5e6; color: #333; margin-top: 20px;">Перейти к оплате</a>
            </p>
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