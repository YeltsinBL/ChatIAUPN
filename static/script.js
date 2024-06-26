const messageBar = document.querySelector(".bar-wrapper input");
const sendBtn = document.querySelector(".bar-wrapper .generar_respuesta");
const messageBox = document.querySelector(".message-box");
const input_message = document.getElementById('input_message')
let respuesta_entrenada=true
let nro_pregunta =0
input_message.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   
   buscar_respuesta(messageBar.value, respuesta_entrenada)
   //buscar_respuesta(verificar_signosinterrogacion(messageBar.value), respuesta_entrenada)
  }
});

sendBtn.onclick = function () {
  buscar_respuesta(messageBar.value, respuesta_entrenada)
  //buscar_respuesta(verificar_signosinterrogacion(messageBar.value), respuesta_entrenada)
}
function verificar_signosinterrogacion(texto){
  const inputText = texto.trim();
    let resultText = inputText;
    if (!inputText.startsWith('¿')) {
        resultText = '¿' + resultText;
    }
    if (!inputText.endsWith('?')) {
        resultText += '?';
    }
    return resultText
}
function buscar_respuesta(UserTypedMessage, entrenado) {
  try {
    nro_pregunta++
    // Ocultar la vista principal y activar la vista de los mensajes
    document.querySelector(".grid-container").classList.add('hidden');
    document.querySelector(".message-box").classList.remove('hidden');
    document.querySelector(".messagebar .bar-wrapper .boton_pdf").classList.remove('hidden');

    //const UserTypedMessage = messageBar.value;
    messageBar.value = "";
    //console.log(entrenado)
    let message =
      `<div class="chat message">
        <img src="static/img/person.png">
        <span>
          ${UserTypedMessage}
        </span>
      </div>`;
    let respuesta = 
      `<div class="chat response">
        <img src="../static/img/upn.svg">
        <div class="respuesta">
          <span class= "new">Obteniendo respuesta...</span>
          <div class="calidad hidden">Si la respuesta no es de de tu agrado, puedes reformularla de diferente forma.</div>
          <div class="multimedia hidden">
            <button id="play_btnVoz" class="boton" onclick="reproducir_voz(this)">
              <img id="img_volume" class="img_volumen" src="../static/img/volume.svg">
              <audio class="audioprueba" src="http://localhost:5000/wav" hidden>
            </button>
            <div class="calidad_tiempo">
              <div class="tiempo">
                <span class="tiempo_span"></span> seg
              </div>
            </div>
          </div>
        </div>
      </div>`
    messageBox.insertAdjacentHTML("beforeend", message);
    messageBox.insertAdjacentHTML("beforeend", respuesta);
    setTimeout(() =>{

    const ChatBotResponse = document.querySelector(".response .new");
    $.ajax({
      type: "POST",
      url: "/",
      data:{mensaje:UserTypedMessage, tipo_entrenado:entrenado, numero_pregunta:nro_pregunta},
      dataType: 'json',
      async: false,
      success: function (data) {
        console.log(data)
        if(entrenado){
          //console.log(data.fin)
          if(data.fin.length >0) {
            let verificar=0
            data.fin.forEach((dato) => {
              const ChatBotResponse = document.querySelector(".response .new");
              //console.log(dato)
              ChatBotResponse.innerHTML = `${dato}`
              if(!dato.includes("Lo siento,")){
                const divs = document.querySelectorAll('.response')
                const lastDiv = divs[divs.length - 1];
                const div_multimedia = lastDiv.querySelector('.multimedia')
                //console.log(div_multimedia)
                const aud = div_multimedia.querySelector('.boton .audioprueba')
                //console.log(aud)
                aud.src="http://localhost:5000/wav/"+data.audio[verificar]
                lector_texto(document.getElementsByClassName("img_volumen"), dato, aud)
                const div_calidad_tiempo = div_multimedia.querySelector('.calidad_tiempo')
                if(data.calidad <= 0.49){
                  lastDiv.querySelector('.calidad').classList.remove('hidden');
                }
                const textSpan = div_calidad_tiempo.querySelector('.tiempo_span')
                textSpan.innerHTML = data.tiempo
                //console.log(textSpan)
                div_multimedia.classList.remove('hidden');
              }
              verificar +=1
              ChatBotResponse.classList.remove("new");
              if(verificar<data.fin.length)messageBox.insertAdjacentHTML("beforeend", respuesta);
            });
          }
          // Crear un elemento ul
          /*const ul = document.createElement('ul')
          ul.classList.add('list-disc', 'pl-5')
          data.fin.forEach((respuesta) => {
            const li = document.createElement('li')
            li.textContent = `${respuesta}`
            ul.appendChild(li);
          });
          // Agregar ul al div
          ChatBotResponse.innerHTML = ""
          ChatBotResponse.appendChild(ul)*/
        }else{
          //messageBox.insertAdjacentHTML("beforeend", respuesta);
          //const ChatBotResponse = document.querySelector(".response .new");
          ChatBotResponse.innerHTML = data.fin
          const divs = document.querySelectorAll('.response .multimedia')
          const lastDiv = divs[divs.length - 1];
          const aud = lastDiv.querySelector('.boton .audioprueba')
          aud.src="http://localhost:5000/wav/"+data.audio
          lector_texto(document.getElementsByClassName("img_volumen"), data.fin, aud)
          lastDiv.classList.remove('hidden');
        }
        ChatBotResponse.classList.remove("new");
      },
      error: function () {
          //console.log('Error en obtener respuestas');
          ChatBotResponse.innerHTML = "Lo siento, no he logrado comprender tu pregunta. Pregunta de nuevo por favor."
          ChatBotResponse.classList.remove("new");
      }
    }, 100);
  // Scroll Automático
  messageBox.scrollTop = messageBox.scrollHeight;
  });
  messageBox.scrollTop = messageBox.scrollHeight;
  } catch (error) {
    console.error(error);
  }
}

// #region Audio
var speechSynth = window.speechSynthesis
var speechUtterance = new SpeechSynthesisUtterance()
speechUtterance.volume = 0
var playBtn = document.querySelector("#img_volume")
volume_off= "../static/img/volume.svg"
volume_on="../static/img/volume_on.svg"

// Reproduciendo
speechUtterance.onstart = function() {
  playBtn.src = volume_on;
  playBtn.style.filter= "invert(1)"
};

//Detenido
speechUtterance.onend = function() {
  playBtn.src = volume_off;
  playBtn.style.filter= "invert(0)"
};
function reproducir_voz(elemento) {
  playBtn = elemento.querySelector("#img_volume")
  valor = elemento.parentNode.parentNode.querySelector('span').innerText
  audio= elemento.querySelector(".audioprueba")

  lector_texto(null,valor,audio)
}
let currentAudio = null
let beforePlayBtn=null
function lector_texto(elemento=null,texto, audio) {
  if(elemento!=null){
    playBtn = elemento[elemento.length-1]
  }
  /*
  speechUtterance.text = texto
  if (speechSynth.speaking && !speechSynth.paused) {
    speechSynth.cancel();
    audio_prueba.muted = true
    audio_prueba.pause()
    audio_prueba.currentTime = 0;
  } else {
    speechSynth.speak(speechUtterance);
    audio_prueba.muted = false
    audio_prueba.play()
  }
*/
  // Pausar el audio actual si está reproduciéndose
  if (currentAudio && currentAudio !== audio) {
    //console.log("Entro a pausar")
    currentAudio.pause();
    currentAudio.currentTime = 0;
    beforePlayBtn.src = volume_off;
    beforePlayBtn.style.filter= "invert(0)"
  }
  if (audio.paused) {
    currentAudio=audio
    audio.play();
    playBtn.src = volume_on;
    playBtn.style.filter= "invert(1)"
    beforePlayBtn= playBtn
  } else {
      currentAudio=null
      audio.pause();
      audio.currentTime = 0;
      playBtn.src = volume_off;
      playBtn.style.filter= "invert(0)"
      beforePlayBtn= playBtn
  }
  audio.addEventListener('ended', () => {
    currentAudio=null
    playBtn.src = volume_off;
    playBtn.style.filter= "invert(0)"
    beforePlayBtn= playBtn
  });

}

// #endregion

// #region Click Div
document.querySelectorAll('.grid-item-two').forEach(div => {
  div.addEventListener('click', function() {
      buscar_respuesta(this.innerText, respuesta_entrenada)
  });
});

const toggleSwitch = document.getElementById('toggle-switch');
const toggleLabel = document.getElementById('toggle-label');
toggleSwitch.addEventListener('change', () => {
    if (toggleSwitch.checked) {
      toggleLabel.textContent = 'Entrenada';
      toggleLabel.style.color='#daa520'
      respuesta_entrenada = true;
    } else {
      toggleLabel.textContent = 'Automática';
      toggleLabel.style.color='#000'
      respuesta_entrenada = false;
    }
});
// #endregion

// #region PDF
function descargar_pdf(elemento){
  //console.log(elemento)
  try {
  elemento.disabled = true;
  elemento.querySelector('.imgboton').style.filter= "invert(50%)"
  //console.log(messageBox.classList.contains('hidden'))
  if(messageBox.classList.contains('hidden')){
    const alertDiv = document.getElementById('alert-div');
            alertDiv.style.display = 'block';
            setTimeout(() => {
                alertDiv.style.display = 'none';
                elemento.disabled = false;
                elemento.querySelector('.imgboton').style.filter= "invert(0)"
            }, 3000); // 3000 milisegundos = 3 segundos
  }else{
    /*event.preventDefault();
    setTimeout(() =>{
    $.ajax({
      type: "POST",
      url: "/pdf",
      //data:{html:document.documentElement.outerHTML},
      //dataType: 'json',
      //async: false,
      xhrFields: {
        responseType: 'blob'
      },
      success: function (data) {
        //console.log(data.fin)
        var blob = new Blob([data], { type: 'application/pdf' });
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'PDF_ChatInteligenteUPN';
        link.click();
      },
      error: function () {
          console.log('Error al genera pdf');
      }
    }, 100);
  });*/
      const childDivs = document.querySelectorAll('.chat');
      let totalHeight = 0;

      childDivs.forEach(div => {
          totalHeight += div.offsetHeight;
      });
      //console.log(totalHeight)
      const { jsPDF } = window.jspdf;

      html2canvas(messageBox, {
          scrollY: -window.scrollY, // Asegura que captura todo el contenido del div
          windowWidth: messageBox.scrollWidth,
          windowHeight: totalHeight*2//messageBox.scrollHeight
      }).then(canvas => {
          const imgData = canvas.toDataURL('image/png');
          const pdf = new jsPDF('p', 'mm', 'a4');
          const pdfWidth = pdf.internal.pageSize.getWidth();
          const pdfHeight = pdf.internal.pageSize.getHeight();
          const imgProps = pdf.getImageProperties(imgData);
          const imgHeight = (imgProps.height * pdfWidth) / imgProps.width;
          let heightLeft = imgHeight;
          let position = 5;
          // Add first page
          pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
          heightLeft -= pdfHeight;
          // Add remaining pages
          while (heightLeft > 0) {
              position = heightLeft - imgHeight + 5;
              pdf.addPage();
              pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
              heightLeft -= pdfHeight;
          }
          pdf.save("PDF_ChatInteligenteUPN.pdf");
          elemento.disabled = false;
          elemento.querySelector('.imgboton').style.filter= "invert(0)"
      });
  }
  } catch (error) {
    console.error(error);
  }
}
// #endregion
