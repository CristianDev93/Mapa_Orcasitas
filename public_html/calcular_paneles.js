map_5b18b0c13fe3401d8901d2c7fb193a32.on('popupopen', function(event) {
    const popup = event.popup;
    const popupContent = popup.getElement();

    // Extraemos el ID 
    const id = popupContent.querySelector('div[data-id]').getAttribute('data-id');

    // Seleccionas los elementos usando los IDs dinámicos
    const boton = popupContent.querySelector(`#btn-calcular-${id}`);
    const consumoAnualInput = popupContent.querySelector(`#consumo-anual-${id}`);
    const potenciaPanelSelect = popupContent.querySelector(`#potencia-panel-${id}`);
    const resultadoCalculo = popupContent.querySelector(`#resultado-calculo-${id}`);
    const iconoEstado = popupContent.querySelector(`#icono-estado-${id}`)
    const tejadoE = popupContent.querySelector(`#tejado-sup-${id}`);
    const tejado = parseFloat(tejadoE.textContent.replace('Tejado disponible:', '').trim());
    const panelP = 1.95;
    const panelM = 2.17;
    const panelG = 2.58;

    if (boton) {
        boton.addEventListener('click', function () {
            console.log('Calculando número de paneles...');
            const consumoAnual = parseFloat(consumoAnualInput.value);
            const potenciaPanel = parseFloat(potenciaPanelSelect.value);
            const horasSolarPico = 5.14;
            let metrosPaneles = 0;
            if (isNaN(consumoAnual) || isNaN(potenciaPanel) || consumoAnual <= 0 || potenciaPanel <= 0) {
                alert('Por favor, ingresa valores válidos.');
                console.error('Valores no válidos:', { consumoAnual, potenciaPanel });
                return;
            }
            
            const numPaneles = (consumoAnual / (horasSolarPico * 365)) / potenciaPanel;
            /*Segun el panel elegido se comptueba si es viable instalarlo en la vivienda teniendo en cuenta la superficie del tejado*/ 
            switch(potenciaPanel){
                
                case 0.44:
                    metrosPaneles = numPaneles * panelP;
                    if(tejado>= metrosPaneles){
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = 'Si hay superficie de tejado para poner los paneles ✔️';
                    }else{
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = 'No hay suficiente superficie de tejado para poner los paneles ❌';
                    }
                    break;
                case 0.49:
                    metrosPaneles = numPaneles * panelM;
                    if(tejado >= metrosPaneles){
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = 'Si hay superficie de tejado para poner los paneles ✔️';
                    }else{
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = 'No hay suficiente superficie de tejado para poner los paneles ❌';
                    }
                    break;
                case 0.59:
                        metrosPaneles = numPaneles * panelG;
                        if(tejado>= metrosPaneles){
                            resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                            iconoEstado.innerText = 'Si hay superficie de tejado para poner los paneles ✔️';
                        }else{
                            resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                            iconoEstado.innerText = `No hay suficiente superficie de tejado para poner los paneles ❌}`;
                        }
                    break;    
            }
            
        });
    } else {
        console.error(`Botón no encontrado dentro del popup para la referencia: ${id}`);
    }
});
