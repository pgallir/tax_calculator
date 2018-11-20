import math

class tassa(object): 
    nome_tassa=None
    def __repr__(self): 
        return self.nome_tassa+':'+str(self.tax)

class inps(tassa):
    nome_tassa='inps'
    # Non iscritti ad altra forma di previdenza obbligatoria 
    # e non pensionati (TUTTI)
    # (dal 2010 	)
    # il tasso pagato dal dipendente e` 1/3 del totale
    tasso = 0.0919 
    def __init__(self, _lordo):
        self.lordo = _lordo
        self.tax = self.compute_tax()

    def compute_tax(self): 
        return self.tasso*self.lordo

class _irpef(tassa): 
    def __init__(self, _imponibile): 
        self.imponibile=_imponibile
        self.compute_tax()

    def compute_tax(self): 
        self.tax = 0
        soglia_precedente=0
        # scaglione e` un dizionario
        # chiave : valore -> limite superiore : tasso irpef
        for soglia,tasso in self.scaglione.items():
            if self.imponibile>soglia:
                self.tax += (soglia-soglia_precedente)*tasso
                soglia_precedente = soglia
            else: 
                self.tax += (self.imponibile-soglia_precedente)*tasso
                break

# REGIONI 
class addizionale_veneto(_irpef): 
    nome_tassa='irpef_addizionale_veneto'
    scaglione = {math.inf:  0.0123}

class addizionale_friuli(_irpef):
    nome_tassa='irpef_addizionale_friuli'
    scaglione = {15000:     0.0070, 
                 math.inf:  0.0123}

class addizionale_emilia_romagna(_irpef):
    nome_tassa='irpef_addizionale_friuli'
    scaglione = {15000:     0.0133, 
                 28000:     0.0193,
                 55000:     0.0203,
                 75000:     0.0223,
                 math.inf:  0.0233}

# COMUNI
class addizionale_verona(_irpef): 
    nome_tassa='irpef_addizionale_verona'
    scaglione = {10000:     0.0000,
                 math.inf:  0.0080}

class addizionale_trieste(_irpef): 
    nome_tassa='irpef_addizionale_trieste'
    scaglione = {12500:     0.000, 
                 math.inf:  0.008}

class addizionale_forli(_irpef):
    nome_tassa='irpef_addizionale_friuli'
    scaglione = { 8000:     0.0000,
                 15000:     0.0060, 
                 28000:     0.0077,
                 55000:     0.0078,
                 75000:     0.0079,
                 math.inf:  0.0080}

class irpef(_irpef):
    nome_tassa='irpef'
    scaglione = {15000:     0.23, 
                 28000:     0.27, 
                 55000:     0.38, 
                 75000:     0.41, 
                 math.inf:  0.43}

class stipendio(object): 
    '''
    https://www.calcolostipendio.it/esempi_calcolo_busta_paga.html
    Reddito imponibile = Reddito annuo lordo - Contributi obbligatori
    Imposta lorda = Irpef + Addizionale Irpef regionale + Addizionale Irpef comunale
    Detrazioni = Detrazione da lovoro dipendente + Detrazione per carichi di famiglia
    Imposta netta = Imposta lorda - Detrazioni
    Reddito netto annuo = Reddito imponibile - Imposta netta
    Stipendio netto mensile = Reddito annuo netto / numero di mensilità
    '''
    def __init__(self,_lordo,_detrazioni,_comune,_regione): 
        self.lordo          = _lordo
        self.inps           = inps(_lordo)
        self.imponibile     = self.lordo-self.inps.tax
        self.detrazioni     = _detrazioni
        self.irpef          = irpef(self.imponibile)
        addizionale_comune  = _comune(self.imponibile)
        addizionale_regione = _regione(self.imponibile)
        self.addizionale    = addizionale_regione.tax + \
                              addizionale_comune.tax
        self.imposta_lorda  = self.irpef.tax+self.addizionale
        self.imposta_netta  = self.imposta_lorda-self.detrazioni
        self.netto          = self.imponibile-self.imposta_netta

    def __repr__(self): 
        return 'lordo:'         + str(self.lordo)         +'\n'+ \
               'inps:'          + str(self.inps.tax)      +'\n'+ \
               'imponibile:'    + str(self.imponibile)    +'\n'+ \
               'detrazioni:'    + str(self.detrazioni)    +'\n'+ \
               'irpef:'         + str(self.irpef.tax)     +'\n'+ \
               'addizionale:'   + str(self.addizionale)   +'\n'+ \
               'imposta_lorda:' + str(self.imposta_lorda) +'\n'+ \
               'imposta_netta:' + str(self.imposta_netta) +'\n'+ \
               'netto:'         + str(self.netto)         +'\n'+ \
               'netto/lordo:'   + str(self.netto/self.lordo) +'\n'+ \
               'perc tasse:'    + str(1-self.netto/self.lordo) +'\n'+ \
               'netto mensile:' + str(self.netto/12)


if __name__ == "__main__": 
    print(stipendio(_lordo=25000,
                    _detrazioni=0,
                    _comune=addizionale_verona,
                    _regione=addizionale_veneto))
