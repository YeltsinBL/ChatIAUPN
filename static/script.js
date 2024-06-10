const messageBar = document.querySelector(".bar-wrapper input");
const sendBtn = document.querySelector(".bar-wrapper button");
const messageBox = document.querySelector(".message-box");
const input_message = document.getElementById('input_message')
let respuesta_entrenada=false
let nro_pregunta =0
input_message.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   buscar_respuesta(messageBar.value, respuesta_entrenada)
  }
});

sendBtn.onclick = function () {
  buscar_respuesta(messageBar.value, respuesta_entrenada)
}

function buscar_respuesta(UserTypedMessage, entrenado) {
  try {
    nro_pregunta++
    // Ocultar la vista principal y activar la vista de los mensajes
    document.querySelector(".grid-container").classList.add('hidden');
    document.querySelector(".message-box").classList.remove('hidden');

    //const UserTypedMessage = messageBar.value;
    messageBar.value = "";
    console.log(entrenado)
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
        <span class= "new">Obteniendo respuesta...</span>
        <button id="play_btnVoz" class="boton" onclick="reproducir_voz(this)">
          <img id="img_volume" class="img_volumen" src="../static/img/volume.svg">
          <audio class="audioprueba" src="http://localhost:5000/wav" hidden>
        </button>
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
          console.log(data.fin)
          // Crear un elemento ul
          const ul = document.createElement('ul')
          ul.classList.add('list-disc', 'pl-5')
          data.fin.forEach((respuesta) => {
            const li = document.createElement('li')
            li.textContent = `${respuesta}`
            ul.appendChild(li);
          });
          // Agregar ul al div
          ChatBotResponse.innerHTML = ""
          ChatBotResponse.appendChild(ul)
        }else{
          ChatBotResponse.innerHTML = data.fin
          const audio_prueba = document.querySelector(".response .boton .audioprueba");
          audio_prueba.src="http://localhost:5000/wav/"+data.audio
          lector_texto(document.getElementsByClassName("img_volumen"), data.fin)
          
          //audio_prueba.controls = true;
          //audio_prueba.play()
        }
        ChatBotResponse.classList.remove("new");
      },
      error: function () {
          console.log('Error en obtener respuestas');
          ChatBotResponse.innerHTML = "Opps! Ha ocurrido un error, por favor intente de nuevo"
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
  valor = elemento.parentNode.querySelector('span').innerText
  lector_texto(null,valor)
}

function lector_texto(elemento=null,texto) {
  const audio_prueba = document.querySelector(".response .boton .audioprueba");
  if(elemento!=null){
    playBtn = elemento[elemento.length-1]
  }
  speechUtterance.text = texto
  if (speechSynth.speaking && !speechSynth.paused) {
    speechSynth.cancel();
    audio_prueba.muted = true
    audio_prueba.pause()
  } else {
    speechSynth.speak(speechUtterance);
    audio_prueba.muted = false
    audio_prueba.play()
  }
}

// #endregion

// #region Click Div
document.querySelectorAll('.grid-item-two').forEach(div => {
  div.addEventListener('click', function() {
      buscar_respuesta(this.innerText, respuesta_entrenada)
  });
});
document.querySelectorAll('.grid-item-botontipo-two').forEach(div => {
  div.addEventListener('click', function() {
      respuesta_entrenada = this.id=="entrenado" ? true:false
  });
});
// #endregion