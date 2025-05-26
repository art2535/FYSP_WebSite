    function showTooltip() {
         var tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'block';
    tooltip.style.opacity = '1';


    setTimeout(function() {
        tooltip.style.transition = 'opacity 1s ease';
    tooltip.style.opacity = '0';


    setTimeout(function() {
        tooltip.style.display = 'none';
         }, 1000);
         }, 3000);
    }
