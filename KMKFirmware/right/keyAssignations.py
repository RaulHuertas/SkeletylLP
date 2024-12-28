from kmk.keys import KC

def assignKeys ():
    
    kc = KC
    NTIL = kc.SCOLON
    OPENING_QUESTION_MARK  = kc.EQUAL
    QUOTE  = kc.MINUS
    OPENING_BRAQUETS  = kc.QUOTE    
    CLOSING_BRAQUETS  = kc.NONUS_HASH 
    LESSER_GREATER = kc.NUBS
    TILDE_DIERESIS = kc.LBRACKET
    PLUS = kc.RBRACKET
    PIPE = kc.GRAVE 
    space = kc.SPACE
    goHome = kc.FD(0)
    noAsg = kc.NO
    lShift = kc.LSHIFT
    
    esc = kc.ESCAPE

    temporal2 = kc.MO(1)
    
    irACapa2 = kc.FD(1)
    irACapa3 = kc.FD(2)


    capa1 = [ noAsg]*40
    
    capa2 = [ noAsg]*40
    
    capa3 = [ noAsg]*40


    #CAPA1
    capa1[0] =  kc.Q
    capa1[1] =  kc.W
    capa1[2] =  kc.E
    capa1[3] =  kc.R
    capa1[4] =  kc.T
    capa1[5] =  kc.Y
    capa1[6] =  kc.U
    capa1[7] =  kc.I
    capa1[8] =  kc.O
    capa1[9] =  kc.P
    
    capa1[10] =  kc.A
    capa1[11] =   kc.S
    capa1[14] =  kc.G

    capa1[15] =  kc.H
    capa1[18] =  kc.L
    capa1[19] =  NTIL
    
    capa1[20] =  kc.Z
    capa1[21] =  kc.X
    capa1[22] =  kc.C
    capa1[23] =  kc.V
    capa1[24] =  kc.B
    capa1[25] =  kc.N
    capa1[26] =  kc.M
    capa1[27] =  kc.COMMA
    capa1[28] =  kc.DOT
    capa1[29] =  kc.SLASH

    capa1[32] =  kc.TAB
    capa1[33] =  kc.SPACE
    capa1[34] =  temporal2
    capa1[35] =  kc.LEFT_SUPER
    capa1[36] =  kc.ENTER
    capa1[37] =  kc.LSHIFT


    #CAPA2
    capa2[0] =  kc.ESC
    capa2[1] =  kc.BSPACE
    capa2[2] =  kc.DELETE
    capa2[3] =  OPENING_BRAQUETS
    capa2[4] =  PLUS
    capa2[5] =  kc.N6
    capa2[6] =  kc.N7
    capa2[7] =  kc.N8
    capa2[8] =  kc.N9
    capa2[9] =  kc.N0
    
    capa2[10] =  TILDE_DIERESIS
    capa2[11] =  OPENING_QUESTION_MARK
    capa2[14] =  PIPE
    
    capa2[15] =  kc.LEFT
    capa2[18] =  kc.RIGHT
    capa2[19] =  LESSER_GREATER
    
    capa2[20] =  kc.F5
    capa2[21] =  kc.F9
    capa2[22] =  kc.F10
    capa2[23] =  kc.F11
    capa2[24] =  kc.F12
    capa2[25] =  kc.N1
    capa2[26] =  kc.N2
    capa2[27] =  kc.N3
    capa2[28] =  kc.N4
    capa2[29] =  kc.N5

    #thumb keys
    capa2[32] =  irACapa3
    capa2[33] =  kc.SPACE
    capa2[34] =  goHome
    capa2[35] =  kc.LEFT_SUPER
    capa2[36] =  kc.ENTER
    capa2[37] =  kc.LSHIFT

    #CAPA3
    capa3[0] =  kc.INSERT
    capa3[1] =  kc.HOME
    capa3[2] =  kc.PGUP
    capa3[3] =  kc.BLE_DISCONNECT
    capa3[4] =  kc.BLE_REFRESH
    capa3[5] =  kc.F6
    capa3[6] =  kc.F7
    capa3[7] =  kc.F8
    capa3[8] =  kc.F9
    capa3[9] =  kc.F10
    
    capa3[10] =  kc.DELETE
    capa3[11] =  kc.END
    capa3[14] =  kc.MEDIA_PLAY_PAUSE 
    capa3[15] =  noAsg
    capa3[18] =  kc.F11
    capa3[19] =  kc.F12
    
    capa3[20] =  kc.AUDIO_MUTE
    capa3[21] =  kc.AUDIO_VOL_DOWN
    capa3[22] =  kc.AUDIO_VOL_UP
    capa3[23] =  kc.MEDIA_PREV_TRACK
    capa3[24] =  kc.MEDIA_NEXT_TRACK
    capa3[25] =  kc.F1
    capa3[26] =  kc.F2
    capa3[27] =  kc.F3
    capa3[28] =  kc.F4
    capa3[29] =  kc.F5

    #thumb keys
    capa3[32] =  kc.TAB
    capa3[33] =  kc.APPLICATION
    capa3[34] =  goHome
    capa3[35] =  kc.LEFT_SUPER
    capa3[36] =  kc.ENTER
    capa3[37] =  kc.LSHIFT

    #HOME ROW MODS
    capa1[13] =   KC.HT(kc.F, kc.LCTRL)
    capa1[16] =   KC.HT(kc.J, kc.RCTRL)
    capa1[12] =   KC.HT(kc.D, kc.LALT)
    capa1[17] =   KC.HT(kc.K, kc.RALT)

    capa2[13] =   KC.HT(CLOSING_BRAQUETS, kc.LCTRL)
    capa2[16] =   KC.HT(kc.DOWN, kc.RCTRL)
    capa2[12] =   KC.HT(QUOTE, kc.LALT)
    capa2[17] =   KC.HT(kc.UP, kc.RALT)

    capa3[13] =  KC.HT(kc.PSCREEN, kc.LCTRL)
    capa3[16] =  KC.HT(noAsg, kc.RCTRL)
    capa3[12] =  KC.HT(kc.PGDOWN, kc.LALT)
    capa3[17] =  KC.HT(noAsg, kc.RALT)

    return  [
        capa1,
        capa2,
        capa3
    ]

