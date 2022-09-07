# -*- coding: utf-8 -*-
###########################################################
# BIBLIOTECAS


# FUNCIONES
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def filtrar_clasificacion(lista):

    nombreGrupo = []
    for grupo in lista:
        if grupo.classificationItem.children is not None:
            nombreGrupo.extend(filtrar_clasificacion(grupo.classificationItem.children))
        else:
            nombreGrupo.append(grupo.classificationItem.id)

    return nombreGrupo