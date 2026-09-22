from app.services.mencoes import detectar_mencoes


def test_detectar_uma_marca():
    texto = "A Acme oferece boas soluções."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
    }


def test_detectar_multiplas_marcas():
    texto = "Acme, Zenith e Nimbus são marcas conhecidas."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
        "Zenith": 1,
        "Nimbus": 1,
    }


def test_detectar_multiplas_ocorrencias_da_mesma_marca():
    texto = (
        "A Acme possui boas soluções. "
        "A Acme também oferece suporte. "
        "A Acme atua em diversos mercados."
    )

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 3,
    }


def test_deteccao_case_insensitive():
    texto = "ACME, acme e AcMe são a mesma marca."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 3,
    }


def test_resposta_sem_marcas():
    texto = "Essa resposta não menciona nenhuma marca monitorada."

    resultado = detectar_mencoes(texto)

    assert resultado == {}


def test_nao_detectar_marca_dentro_de_outra_palavra():
    texto = "O termo Acme aparece, mas Acme123 não deve ser considerado."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
    }


def test_detectar_marcas_em_texto_com_pontuacao():
    texto = "Acme! Zenith? Nimbus."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
        "Zenith": 1,
        "Nimbus": 1,
    }


def test_texto_vazio():
    resultado = detectar_mencoes("")

    assert resultado == {}
