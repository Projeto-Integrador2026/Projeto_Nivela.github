// Nivela — Nivelamento de Python (tela animada)
//
// ATENÇÃO — PROTÓTIPO: as perguntas e o gabarito ("correta") estão aqui só
// para validar o visual e a animação. No projeto final o gabarito NÃO pode
// ir para o navegador (qualquer pessoa leria as respostas no DevTools).
// Na etapa do backend:
//   1) as perguntas passam a vir do servidor SEM o campo "correta";
//   2) a função avaliar() faz um POST e o Django calcula o nível.
// Só a função avaliar() precisa mudar; o resto da tela continua igual.

(function () {
  "use strict";

  var PERGUNTAS = [
    {
      enunciado: "Qual é a saída deste código?",
      codigo: "print(type(3.0))",
      alternativas: ["<class 'int'>", "<class 'str'>", "<class 'float'>", "Erro"],
      correta: 2
    },
    {
      enunciado: "Qual é a saída deste código?",
      codigo: 'print(len("nivela"))',
      alternativas: ["5", "7", "Erro", "6"],
      correta: 3
    },
    {
      enunciado: "Qual é a saída deste código?",
      codigo: 'for i in range(3):\n    print(i, end=" ")',
      alternativas: ["1 2 3", "0 1 2", "0 1 2 3", "1 2"],
      correta: 1
    },
    {
      enunciado: "O que este código imprime?",
      codigo: 'd = {"a": 1}\nprint(d.get("b", 0))',
      alternativas: ["None", "KeyError", "1", "0"],
      correta: 3
    },
    {
      enunciado: "Qual é o resultado?",
      codigo: 'print(bool("False"))',
      alternativas: ["True", "False", "Erro", "None"],
      correta: 0
    },
    {
      enunciado: "O que será impresso?",
      codigo: "a = [1, 2]\nb = a\nb.append(3)\nprint(a)",
      alternativas: ["[1, 2, 3]", "[1, 2]", "[3]", "Erro"],
      correta: 0
    },
    {
      enunciado: "Qual é o resultado desta list comprehension?",
      codigo: "print([n * 2 for n in range(4) if n % 2 == 0])",
      alternativas: ["[0, 2, 4, 6]", "[2, 4]", "[0, 4]", "[0, 2]"],
      correta: 2
    },
    {
      enunciado: "O que este código imprime?",
      codigo: "def f(x, lista=[]):\n    lista.append(x)\n    return lista\n\nf(1)\nprint(f(2))",
      alternativas: ["[2]", "[1]", "Erro", "[1, 2]"],
      correta: 3
    }
  ];

  var NIVEIS = {
    1: { nome: "Iniciante",     texto: "Você está começando agora, e tudo bem! A turma vai te guiar do zero." },
    2: { nome: "Básico",        texto: "Você já conhece o essencial. Vamos consolidar as bases." },
    3: { nome: "Intermediário", texto: "Boa base! Falta pouco para dominar os detalhes da linguagem." },
    4: { nome: "Avançado",      texto: "Excelente! Você domina até as pegadinhas do Python." }
  };

  // Único ponto que muda quando o backend existir (trocar por fetch/POST).
  function avaliar(respostas) {
    return new Promise(function (resolve) {
      var acertos = 0;
      PERGUNTAS.forEach(function (p, i) {
        if (respostas[i] === p.correta) { acertos++; }
      });
      var nivel = acertos >= 7 ? 4 : acertos >= 5 ? 3 : acertos >= 3 ? 2 : 1;
      resolve({ acertos: acertos, total: PERGUNTAS.length, nivel: nivel });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var raiz = document.getElementById("nv-quiz");
    if (!raiz) { return; }

    var reduzMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var DURACAO = reduzMovimento ? 0 : 260;
    var LETRAS = ["A", "B", "C", "D"];
    var ALTURAS = [70, 105, 140, 175];

    var painel = raiz.querySelector(".nv-quiz-card");
    var etapas = {
      intro: raiz.querySelector('[data-etapa="intro"]'),
      pergunta: raiz.querySelector('[data-etapa="pergunta"]'),
      resultado: raiz.querySelector('[data-etapa="resultado"]')
    };

    var contador = document.getElementById("nv-contador");
    var trilha = document.getElementById("nv-trilha");
    var trilhaFill = document.getElementById("nv-trilha-fill");
    var enunciado = document.getElementById("nv-enunciado");
    var codigo = document.getElementById("nv-codigo");
    var opcoes = document.getElementById("nv-opcoes");
    var btnProxima = document.getElementById("nv-proxima");
    var degraus = raiz.querySelectorAll(".nv-degrau");

    var indice = 0;
    var respostas = [];
    var ocupado = false;

    function mostrarEtapa(nome) {
      Object.keys(etapas).forEach(function (chave) {
        etapas[chave].hidden = (chave !== nome);
      });
    }

    // Anima a saída do conteúdo atual, troca o conteúdo e anima a entrada.
    function transicao(atualizar) {
      painel.classList.add("is-saindo");
      window.setTimeout(function () {
        atualizar();
        painel.classList.remove("is-saindo");
        painel.classList.add("is-entrando");
        window.setTimeout(function () { painel.classList.remove("is-entrando"); }, DURACAO);
        var alvo = painel.querySelector("[data-etapa]:not([hidden]) [data-foco]");
        if (alvo) { alvo.focus({ preventScroll: true }); }
      }, DURACAO);
    }

    function renderPergunta() {
      var p = PERGUNTAS[indice];
      var total = PERGUNTAS.length;

      contador.textContent = "Pergunta " + (indice + 1) + " de " + total;
      trilha.setAttribute("aria-valuemin", "0");
      trilha.setAttribute("aria-valuemax", String(total));
      trilha.setAttribute("aria-valuenow", String(indice + 1));
      trilhaFill.style.width = ((indice + 1) / total * 100) + "%";

      enunciado.textContent = p.enunciado;

      if (p.codigo) {
        codigo.textContent = p.codigo; // textContent: nunca interpreta HTML
        codigo.hidden = false;
      } else {
        codigo.hidden = true;
      }

      opcoes.innerHTML = "";
      p.alternativas.forEach(function (texto, i) {
        var botao = document.createElement("button");
        botao.type = "button";
        botao.className = "nv-opcao";
        botao.setAttribute("role", "radio");
        botao.setAttribute("aria-checked", "false");
        botao.style.setProperty("--i", String(i));

        var letra = document.createElement("span");
        letra.className = "nv-opcao-letra";
        letra.textContent = LETRAS[i];

        var conteudo = document.createElement("span");
        conteudo.className = "nv-opcao-texto";
        conteudo.textContent = texto;

        botao.appendChild(letra);
        botao.appendChild(conteudo);
        botao.addEventListener("click", function () { selecionar(i); });
        opcoes.appendChild(botao);
      });

      btnProxima.disabled = true;
      btnProxima.textContent = (indice === total - 1) ? "Ver meu nível" : "Próxima";
    }

    function selecionar(i) {
      respostas[indice] = i;
      Array.prototype.forEach.call(opcoes.children, function (el, k) {
        var ativa = (k === i);
        el.classList.toggle("is-selecionada", ativa);
        el.setAttribute("aria-checked", ativa ? "true" : "false");
      });
      btnProxima.disabled = false;
    }

    function avancar() {
      if (ocupado || respostas[indice] === undefined) { return; }
      if (indice < PERGUNTAS.length - 1) {
        ocupado = true;
        transicao(function () {
          indice++;
          renderPergunta();
          ocupado = false;
        });
      } else {
        finalizar();
      }
    }

    function finalizar() {
      ocupado = true;
      btnProxima.disabled = true;
      avaliar(respostas).then(function (resultado) {
        transicao(function () {
          mostrarEtapa("resultado");
          renderResultado(resultado);
          ocupado = false;
        });
        window.setTimeout(function () { animarDegraus(resultado.nivel); }, DURACAO * 2 + 150);
      }).catch(function (erro) {
        console.error("Falha ao avaliar o nivelamento:", erro);
        ocupado = false;
        btnProxima.disabled = false;
      });
    }

    function renderResultado(r) {
      var info = NIVEIS[r.nivel];
      document.getElementById("nv-res-titulo").textContent = "Nível " + r.nivel + " · " + info.nome;
      document.getElementById("nv-res-texto").textContent = info.texto;
      document.getElementById("nv-res-acertos").textContent = r.acertos + " de " + r.total + " acertos";

      // zera a escada para a animação rodar de novo ao refazer
      Array.prototype.forEach.call(degraus, function (el) {
        el.style.height = "0px";
        el.classList.remove("is-atingido");
      });
    }

    function animarDegraus(nivel) {
      Array.prototype.forEach.call(degraus, function (el, i) {
        window.setTimeout(function () {
          el.style.height = ALTURAS[i] + "px";
          el.classList.toggle("is-atingido", i < nivel);
        }, reduzMovimento ? 0 : i * 150);
      });
    }

    function reiniciar() {
      if (ocupado) { return; }
      ocupado = true;
      transicao(function () {
        indice = 0;
        respostas = [];
        mostrarEtapa("pergunta");
        renderPergunta();
        ocupado = false;
      });
    }

    document.getElementById("nv-comecar").addEventListener("click", function () {
      if (ocupado) { return; }
      ocupado = true;
      transicao(function () {
        mostrarEtapa("pergunta");
        renderPergunta();
        ocupado = false;
      });
    });

    btnProxima.addEventListener("click", avancar);
    document.getElementById("nv-refazer").addEventListener("click", reiniciar);

    // Atalho: teclas 1-4 escolhem a alternativa e levam o foco ao botão "Próxima".
    document.addEventListener("keydown", function (e) {
      if (etapas.pergunta.hidden || ocupado) { return; }
      if (e.ctrlKey || e.metaKey || e.altKey) { return; }
      var n = parseInt(e.key, 10);
      if (n >= 1 && n <= PERGUNTAS[indice].alternativas.length) {
        selecionar(n - 1);
        btnProxima.focus({ preventScroll: true });
      }
    });

    mostrarEtapa("intro");
  });
})();
