# -*- coding: utf-8 -*-
###########################################################
# BIBLIOTECAS
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import clr  # CommonLanguage Runtime

# Para trabajar con la RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

# Para trabajar con la RevitAPIUI
clr.AddReference('RevitAPIUI')
import Autodesk  # noqa: E402
from Autodesk.Revit.UI import *

# Para trabajar contra el documento y hacer transacciones
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Identificadores
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication  # interfaz
uidoc = uiapp.ActiveUIDocument  # Para que el usuario interactue con el doc

# Otras bibliotecas
import System
from System.Collections.Generic import List  # Para generar iList


# FUNCIONES
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Operaciones con listas
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def aLista(arg):
    """
    Uso: Evita errores con la entrada de inputs.
    Me convierte a lista si no lo era.
    """
    if hasattr(arg, '__iter__'):
        return arg
    else:
        return [arg]


def flatten(lista):
    """
    Uso: Aplanado de lista con multiples sub niveles.
    """
    salida = []
    for x in lista:
        if hasattr(x, "__iter__"):
            salida.extend(flatten(x))
        else:
            salida.append(x)
    return salida


def profundidadLista1(lista):
    """
    Uso: Pregunta el nivel de profundidad de una lista.
    Entrada: lista <list>: Lista.
    Salida: Numero.
    """
    funcion = lambda sublista: isinstance(sublista, list) and max(map(
        funcion, sublista)) + 1
    return funcion(lista)


def unique_items(lista):
    """
    Uso: Crea una lista con los elementos unicos, mantiene el orden.
    Entrada:
        lista <List>
    """
    claves = []
    for item in lista:
        if item not in claves:
            claves.append(item)


def agrupar_por_clave(lista, indice=0):
    """
    Uso: Agrupa una lista por una clave en el indice especificado.
    Entrada:
        lista <List>
        indice <Integer>: indice de la clave en la lista.
    Salida: lista <List> agrupada por clave.
    """
    listaIndice = map(lambda x: x[indice], lista)
    values = unique_items(listaIndice)
    return [[y for y in lista if y[indice] == x] for x in values]


def agrupar_por_lista(lista, listaClave):
    """
    Uso: Agrupa una lista por una lista de claves.
    Entrada:
        lista <List>
        listaClave <List>
    Salida: lista <List> agrupada por clave.
    """
    lookup = {}  # lookup map
    result = []
    for k, l in zip(listaClave, lista):
        if k not in lookup:
            target = lookup[k] = [l]
            result.append(target)
        else:
            lookup[k].append(l)
    return result


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Listados
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def listado_builtincategory():
    """
    Uso: Listado de las BuiltInCategory de Revit.
    """
    return System.Enum.GetValues(BuiltInCategory)


def listado_builtinparameter():
    """
    Uso: Listado de las BuiltInParameter de Revit.
    """
    return System.Enum.GetValues(BuiltInParameter)


def listado_categorias():
    """
    Uso: Genera un diccionario con todas las categorias de Revit.
    Salida: Diccionario(clave: nombre, valor: categoria)
    """
    diccionario = {}
    categorias = doc.Settings.Categories
    for cat in categorias:
        diccionario[cat.Name] = cat
    return diccionario


def listado_plantillas_vista(documento=doc):
    """
    Uso: Obtener el listado de todas las plantillas de vista.
    Entrada: Documento del que se obtiene el listado.
    Salida: Diccionario(clave: nombre plantilla, valor: id).
    """
    salida = dict()
    for vista in FilteredElementCollector(documento).OfClass(View):
        if vista.IsTemplate:
            salida[vista.Name] = vista.Id
    return salida


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Filtros
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def bic_por_nombreVisual(nombre):
    """
    Uso: Busca la BuiltInCategory que coincide con el nombre dado.
    Entrada: Nombre de la categoria a buscar <string>.
    Salida: BuiltInCategory <BuiltInCategory>.
    """
    values = System.Enum.GetValues(BuiltInCategory)

    def catch(default, function, *args, **kwargs):
        try: return function(*args, **kwargs)
        except: return default

    valuesRevit = map(lambda x: catch(None, LabelUtils.GetLabelFor, x), values)
    dictionary = dict(zip(valuesRevit, values))
    return dictionary[nombre]


def bic_por_nombreBuilt(nombre):
    """
    Uso: Busca la BuiltInCategory que coincide con el nombre dado.
    Entrada: Nombre de la BuiltInCategory (a partir del punto) a buscar <string>.
    Salida: BuiltInCategory <BuiltInCategory>.
    """
    values = System.Enum.GetValues(BuiltInCategory)
    names = System.Enum.GetNames(BuiltInCategory)

    dictionary = dict(zip(names, values))
    return dictionary[nombre]


def bip_por_nombreVisual(nombre):
    """
    Uso: Busca el BuiltInParameter que coincide con el nombre dado.
    Entrada: Nombre del parametro a buscar <string>.
    Salida: BuiltInParameter <BuiltInParameter>.
    """
    values = System.Enum.GetValues(BuiltInParameter)

    def catch(default, function, *args, **kwargs):
        try: return function(*args, **kwargs)
        except: return default

    valuesRevit = map(lambda x: catch(None, LabelUtils.GetLabelFor, x), values)
    dictionary = dict(zip(valuesRevit, values))
    return dictionary[nombre]


def bip_por_nombreBuilt(nombre):
    """
    Uso: Busca el BuiltInParameter que coincide con el nombre dado.
    Entrada: Nombre del BuiltInParameter (a partir del punto) a buscar <string>.
    Salida: BuiltInParameter <BuiltInParameter>.
    """
    values = System.Enum.GetValues(BuiltInParameter)
    names = System.Enum.GetNames(BuiltInParameter)

    dictionary = dict(zip(names, values))
    return dictionary[nombre]


def parUser_por_nombre(nombre):
    """
    Uso: Obtiene un parametro de usuario por nombre.
    Entrada: nombre <str>: Nombre del parametro.
    Salida: Id del parametro <ElementId>.
    """
    iterador = doc.ParameterBindings().ForwardIterator()
    while iterador.MoveNext():
        if iterador.Key.Name == nombre:
            par = iterador.Key.Id
    return par


def filtroParametroPers(nombre, valor):
    """
    Uso: Crea un filtro para el FilteredElementCollector.
    Entrada:
        nombre <str>: Nombre del parametro.
        valor <str>: Valor del parametro.
    Salida: Filtro para aplicar en FilteredElementCollector con .WherePasses()
    """
    iterador = doc.ParameterBindings().ForwardIterator()
    while iterador.MoveNext():
        if iterador.Key.Name == nombre:
            proveedor = ParameterValueProvider(iterador.Key.Id)
            break
    evaluador = FilterStringEquals()
    regla = FilterStringRule(proveedor, evaluador, valor)
    return ElementParameterFilter(regla)


def filtrar_vista_por_nombre(nombre):
    """
    Uso:
    Entrada:
        nombre <str>: El nombre de la vista a filtrar
    Salida: La vista <View>
    """
    salida = dict()
    colector = FilteredElementCollector(doc).OfClass(View).ToElements()
    # Se limpian las plantillas y los nulos
    for vista in colector:
        if vista.IsTemplate is not True:
            salida[vista.Name] = vista
    # Seguro para evitar errores
    try:
        return salida[nombre]
    except:
        return 'Error: revisar nombre de entrada.'


def filtrar_vista_por_tipo(nombre):
    """
    Uso: Filtra las vistas por el tipo dado.
    Entrada: nombre <str>
    """
    salida = "Revisar valor entrada"
    tiposVistas = System.Enum.GetValues(ViewType)
    for tipo in tiposVistas:
        if nombre == str(tipo):
            vistas = FilteredElementCollector(doc).OfClass(View)
            salida = [v for v in vistas if v.ViewType == tipo]

    return salida


def filtrar_patron_por_nombre(nombre):
    """
    Uso: Selecciona el patron de relleno por nombre, si existe.
    Entrada:
        nombre <str>: El nombre del patron a seleccionar
    Salida: La vista <View>
    """
    salida = None
    colector = (
        FilteredElementCollector(doc).OfClass(FillPatternElement).
        ToElements())
    # Se revisa el nombre de los filtros
    for filtro in colector:
        if filtro.Name == nombre:
            salida = filtro
    return salida


def filtrar_esquema_por_nombre(nombre):
    """
    Uso: Selecciona el esquema de area por nombre, si existe.
    Entrada:
        nombre <str>: El nombre deL esquema a seleccionar
    Salida: La vista <View>
    """
    salida = None
    colector = (
        FilteredElementCollector(doc).OfClass(AreaScheme).
        ToElements())
    # Se revisa el nombre de los filtros
    for esquema in colector:
        if esquema.Name == nombre:
            salida = esquema
    return salida


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Utilidades
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def catch(default, function, *args, **kwargs):
    """
    Uso:
        Atrapa errores convirtiendolos en Null. Para map() o list
        comprehension sin fallos.
    Entrada:
        default: Sustituto del error.
        function: Funcion (sin parentesis).
        *args = Elemento sobre el que aplicar la funcion.
    Salida: Filtro para aplicar en FilteredElementCollector con .WherePasses()
    """
    try: return function(*args, **kwargs)
    except: return default


def parametro_valor(par):
    """
    Uso: Obtener el valor de cualquier parametro, sea cual sea su Storage.
    Entrada:
        par <Parameter>: Parametro a consultar su valor.
    Salida: El valor del parametro.
    """
    if par is not None:
        if par.StorageType == StorageType.String:
            valor = par.AsString()
        elif par.StorageType == StorageType.Double:
            valor = par.AsDouble()
        elif par.StorageType == StorageType.Integer:
            valor = par.AsInteger()
        elif par.StorageType == StorageType.ElementId:
            valor = doc.GetElement(par.AsElementId())
        else:
            valor = par.AsValueString()
    else: valor = None
    return valor


def valor_parametro_multiple(e, nombre):
    """
    Uso: Lee todos los parametros que coinciden con el nombre dado, y obtiene
    un valor que no sea nulo.
    Entrada: e <Element>
             nombre <string>
    """
    for par in e.GetParameters(nombre):
        if par.AsString() != "" and par.AsString() is not None:
            return par.AsString()


def diccionario_agrupar_por_clave(claves, valores):
    """
    Uso:
        Genera un diccionario. En la lista de claves hay multiples items
        repetidos, por lo tanto los valores se agrupan.
    Entrada:
        claves <List[string]>
        valores <List>
    Salida:
        Diccionario con valores agrupados por clave <dict>
    """
    diccionario = dict()
    for a, b in zip(claves, valores):
        if a in diccionario:
            diccionario[a].append(b)
        else:
            diccionario[a] = list()
            diccionario[a].append(b)
    return diccionario


def obtener_tipo(elemento):
    """
    Uso: Obtiene el tipo desde un elemento.
    """
    tipo = doc.GetElement(elemento.GetTypeId())
    return tipo


def punto_XYZ(x=0, y=0, z=0):
    """
    Uso: Crea un XYZ() en metros, y lo convierte a unidades internas.
    Cuidado: Dependencia de la funcion unidades_modelo_a_internas_longitud().
    """
    factor = unidades_modelo_a_internas_longitud(1)
    return XYZ(x, y, z).Multiply(factor)


def color_consultar_rgb(color):
    """
    Uso: Consulta los valores rgb.
    Salida: Canales rgb en formato string.
    """
    if isinstance(color, Color):
        # Se revisa si el color es valido o no ha sido definido por el usuario
        if color.IsValid:
            salida = "(%s, %s, %s)" % (color.Red, color.Green, color.Blue)
        else:
            salida = -1
    else:
        salida = 'Se esperaba <Autodesk.Revit.DB.Color>'
    return salida


def natural_keys(texto):
    """
    Uso: Convierte un texto en letras y numeros para su orden natural.
    Entrada: texto <string>
    Salida: lista con caracteres del texto separados.
    """
    from re import split

    def atoi(texto):
        return int(texto) if texto.isdigit() else texto

    return [atoi(c) for c in split(r'(\d+)', texto)]


def elimina_tildes(texto):
    """
    Uso: Elimina las tildes de un texto.
    Entrada: texto <string>
    """
    import unicodedata
    s = ''.join((c for c in unicodedata.normalize('NFD', texto)
                 if unicodedata.category(c) != 'Mn'))
    return s




# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Utilidades VISTAS
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def vista_aplicar_configuracion_deotra(vista, configuracion):
    """
    Uso: Aplica la configuracion de la vista configuracion.
    Entrada:
        vista <View>
        configuracion <View>
    """
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
        vista.ApplyViewTemplateParameters(configuracion)
        TransactionManager.Instance.TransactionTaskDone()
        return 'Completado'
    except:
        return 'Fallo: revisar tipos de vista.'


def vista_definir_vista_activa(vista):
    """
    Uso: Forzar que una vista en concreto sea la vista activa.
    Entrada: vista <View>
    """
    TransactionManager.Instance.ForceCloseTransaction()
    try:
        uidoc.RequestViewChange(vista)
        return 'Completado'
    except:
        return 'Fallo'


def id_tipo_familia_vista():
    """
    Uso: Obtiene el id de la familia de vista dada.
    """
    colector = (FilteredElementCollector(doc).OfClass(ViewFamilyType).
                ToElements())
    ids = [tipo.Id for tipo in colector]
    nombres = [str(tipo.ViewFamily) for tipo in colector]
    return dict(zip(nombres, ids))


def limpieza_vistas_sin_uso(inicio, prefijo='', opcionTablas=True):
    """
    Uso: Se eliminan las vistas sin uso, teniendo en cuenta anfitrio de vistas.
    dependientes, de llamada...
    Entrada: inicio <boolean>
    Salida: Resultado
    """
    if inicio:
        # Colectar los planos
        planos = FilteredElementCollector(doc).OfClass(ViewSheet)
        # Se consultan las vistas dentro de los planos
        idsvistasPlanos = [p.GetAllPlacedViews() for p in planos]
        # Aplano
        idsUsados = [v for lista in idsvistasPlanos for v in lista]

        # Reviso la dependencia
        idsDepen = [doc.GetElement(v).GetPrimaryViewId() for v in idsUsados]
        for id in idsDepen:
            if str(id) != '-1' and id not in idsUsados: 
                idsUsados.append(id)

        # Reviso callouts
        idsCalloutanfi = [doc.GetElement(id).get_Parameter(BuiltInParameter.SECTION_PARENT_VIEW_NAME) for id in idsUsados]
        for parametro in idsCalloutanfi:
            if parametro != None:
                id = parametro.AsElementId()
                if id != ElementId(-1) and id not in idsUsados:
                    idsUsados.append(parametro.AsElementId())

        # Se incorporan los planos
        for plano in planos:
            idsUsados.append(plano.Id)

        # Se trabaja con las tablas
        if opcionTablas:
            # Se conservan las tablas
            tablas = FilteredElementCollector(doc).OfClass(ViewSchedule).ToElements()
            if tablas:
                for t in tablas:
                    idsUsados.append(t.Id)
        else:
            # Se quiere eliminar todas las tablas sin uso
            tablas = FilteredElementCollector(doc).OfClass(ScheduleSheetInstance)
            if tablas:
                for t in tablas:
                    idsUsados.append(t.ScheduleId)            

        # Colectar todas las vistas
        vistas = FilteredElementCollector(doc).OfClass(View).ToElements()
        # Descartar plantillas de vistas
        vistasIds = []
        for v in vistas:
            if v.IsTemplate is False:
                if v.Name.startswith(prefijo) is False and v.ViewType != ViewType.SystemBrowser and v.ViewType != ViewType.ProjectBrowser:
                    vistasIds.append(v.Id)

        # Resto la lista que quiero mantener a la de vistas a eliminar
        lista1 = set(idsUsados)
        lista2 = set(vistasIds)
        idsNoUsados = lista2.difference(lista1)

        contador = 0
        if idsNoUsados:
            TransactionManager.Instance.EnsureInTransaction(doc)
            for id in idsNoUsados:
                try:
                    doc.Delete(id)
                    contador = contador + 1
                except:
                    pass
            TransactionManager.Instance.TransactionTaskDone()

        if contador == 0 and len(idsNoUsados) != 0:
            salida = 'Existen {} vistas sin usar y no se ha eliminado ninguna.'.format(len(idsNoUsados))
        elif contador > 0:
            salida = 'Se han eliminado {} vistas de {} vistas posibles.'.format(contador, len(idsNoUsados))
        else:
            salida = 'No hay vistas sin uso'

    else:
        salida = 'Aviso: Para iniciar la ejecución necesita un True.'

    return salida


def limpieza_plantillas_vista(inicio):
    """
    Uso: Se eliminan las plantillas sin uso.
    """
    if inicio:
        plantillas, plantillasUso = set(), set()
        for vista in FilteredElementCollector(doc).OfClass(View).ToElements():
            if vista.IsTemplate:
                plantillas.add(vista.Id)
            else:
                if vista.ViewTemplateId != ElementId(-1):
                    plantillasUso.add(vista.ViewTemplateId)

        # Hacemos la diferencia de conjuntos
        sinUso = plantillas.difference(plantillasUso)
        limpieza = List[ElementId](sinUso)
        # Revisamos el contenido de sinUso
        if limpieza:
            try:
                TransactionManager.Instance.EnsureInTransaction(doc)
                doc.Delete(limpieza)
                TransactionManager.Instance.TransactionTaskDone()
                salida = 'Completado'
            except:
                salida = 'Fallo: En la eliminación.'
        else:
            salida = 'Completado.\nNo existen plantillas sin uso.'
    else:
        salida = 'Aviso: Para iniciar la ejecución necesita un True.'

    return salida


def vista_crear_plantilla(lista):
    """
    Uso:
        Crear una o varias plantilla/s de vista partiendo de una
        o multiples vistas.
    Entrada:
        lista <>: Desconocemos si nos dan una vista o una lista de vistas.
    Salida: Plantilla/s de vista creada/s.
    Cuidado: Dependencia de la funcion aLista().
    """
    vistas = aLista(lista)
    TransactionManager.Instance.EnsureInTransaction(doc)
    salida = [vista.CreateViewTemplate() for vista in vistas]
    TransactionManager.Instance.TransactionTaskDone()
    return salida


def graficos_aislar_elementos_temporal(lista, vista=doc.ActiveView):
    """
    Uso: 
    Entrada:
        lista <>: Desconocemos si nos daran una vista o una lista de vistas.
        vista <View>: valor por defecto la vista activa.
    Salida: Mensaje exito/fallo.
    Cuidado: Dependencia de la funcion aLista().
    """
    elementos = aLista(lista)
    idsLista = List[ElementId]()
    for e in elementos:
        idsLista.Add(e.Id)
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
        vista.IsolateElementsTemporary(idsLista)
        salida = 'Completado'
        TransactionManager.Instance.TransactionTaskDone()
    except:
        salida = None
    return salida


def graficos_aislar_elementos(lista, vista=doc.ActiveView):
    """
    Uso:
    Entrada:
        lista <>: Desconocemos si nos daran una vista o una lista de vistas.
        vista <View>: valor por defecto la vista activa.
    Salida: Mensaje exito/fallo.
    Cuidado: Dependencia de la funcion aLista().
    """
    elementos = aLista(lista)
    idsLista = List[ElementId]()
    for e in elementos:
        idsLista.Add(e.Id)
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
        vista.IsolateElementsTemporary(idsLista)
        vista.ConvertTemporaryHideIsolateToPermanent()
        salida = 'Completado'
        TransactionManager.Instance.TransactionTaskDone()
    except:
        salida = None
    return salida


def vista_opciones_duplicado(integer):
    """
    Uso: Selecciona un ViewDuplicateOption.
         1 = Duplicate   2 = AsDependent   3 = WithDetailing
    """
    opciones = System.Enum.GetValues(ViewDuplicateOption)

    if integer <= 2:
        return opciones[integer]
    else:
        return 'Fallo: Introducir un valor entre 0 y 2.'


def vista_duplicar(lista, opciones=1, prefijo='', sufijo=''):
    """
    Uso:
    Entrada:
        lista <>: Desconocemos si nos daran una vista o una lista de vistas.
        opciones <int>: Opciones de duplicado.
        prefijo <str>: Prefijo para el nombre de la vista.
        sufijo <str>: Prefijo para el nombre de la vista.
    Salida: Mensaje exito/fallo.
    Cuidado: Dependencia de la funcion aLista() y vista_opciones_duplicado().    
    """
    vistas = aLista(lista)

    salida = []
    TransactionManager.Instance.EnsureInTransaction(doc)
    for vista in vistas:
        if not vista.IsTemplate:
            id = vista.Duplicate(vista_opciones_duplicado(opciones))
            nueva = doc.GetElement(id)
            try:
                nueva.Name = str(prefijo) + vista.Name + str(sufijo)
            except:
                pass
            salida.append(nueva)
    TransactionManager.Instance.TransactionTaskDone()

    return salida


def vista_consultar_modificaciones_filtros(vista):
    """
    Uso:
        Se revisa la vista y se extrae la informacion sobre los filtros y que
        modificaciones se estan haciendo en la visibilidad grafica.
    Entradas:
        vista <View>: Vista a revisar
    Salida:
        Se genera un diccionario con diccionarios anidados, para acceder por
        clave a cualquier configuracion dentro de cualquier filtro.
    """     
    salida = dict()
    if isinstance(vista, View) and vista.IsTemplate is False:
        try:
            # Se buscan los filtros
            filtros = vista.GetFilters()
            # Se condiciona el siguiente paso: deben haber filtros
            if filtros:
                for id in filtros:
                    datos = dict()
                    # Se consulta el nombre
                    # Sera la clave para acceder al filtro
                    filtro = doc.GetElement(id)
                    nombreFiltro = filtro.Name
                    # Se consulta si esta visible y activo el filtro
                    datos['Visible'] = vista.GetFilterVisibility(id)
                    datos['Activo'] = vista.GetIsFilterEnabled(id)

                    # Se accede a las modificaciones
                    configuracion = vista.GetFilterOverrides(id)
                    # Se va a generar un sistema de diccionarios anidados

                    # Informacion de proyeccion
                    proyeccion = dict()
                    # Informacion de las lineas
                    lineasProyeccion = dict()
                    lineasProyeccion['Patrón'] = (
                        configuracion.ProjectionLinePatternId)
                    lineasProyeccion['Color'] = (
                        color_consultar_rgb(
                            configuracion.ProjectionLineColor))
                    lineasProyeccion['Grosor'] = (
                        configuracion.ProjectionLineWeight)
                    # Se almacena la informacion de las lineas de proyeccion
                    proyeccion['Líneas'] = lineasProyeccion
                    # Informacion de los patrones de superficie
                    patronesProyeccion = dict()
                    # Primero lo relativo al patron primer plano
                    patronesProyeccion['Primer plano - Visibilidad'] = (
                        configuracion.IsSurfaceForegroundPatternVisible)
                    patronesProyeccion['Primer plano - Patrón'] = (
                        configuracion.SurfaceForegroundPatternId)
                    patronesProyeccion['Primer plano - Color'] = (
                        color_consultar_rgb(
                            configuracion.SurfaceForegroundPatternColor))
                    # Lo relativo al patron de fondo
                    patronesProyeccion['Fondo - Visibilidad'] = (
                        configuracion.IsCutForegroundPatternVisible)
                    patronesProyeccion['Fondo - Patrón'] = (
                        configuracion.CutForegroundPatternId)
                    patronesProyeccion['Fondo - Color'] = (
                        color_consultar_rgb(
                            configuracion.CutForegroundPatternColor))
                    # Se almacena la informacion de las lineas de proyeccion
                    proyeccion['Patrones'] = patronesProyeccion
                    # Tercero: transparencia
                    proyeccion['Transparencia'] = configuracion.Transparency
                    # Se almacena toda la informacion relativa a proyeccion
                    datos['Proyeccion'] = proyeccion

                    # Informacion de corte
                    corte = dict()
                    # Informacion de las lineas
                    lineasCorte = dict()
                    lineasCorte['Patrón'] = (
                        configuracion.CutLinePatternId)
                    lineasCorte['Color'] = (
                        color_consultar_rgb(configuracion.CutLineColor))
                    lineasCorte['Grosor'] = (
                        configuracion.CutLineWeight)
                    # Se almacena la informacion de las lineas de proyeccion
                    corte['Líneas'] = lineasCorte
                    # Informacion de los patrones de superficie
                    patronesCorte = dict()
                    # Primero lo relativo al patron primer plano
                    patronesCorte['Primer plano - Visibilidad'] = (
                        configuracion.IsSurfaceBackgroundPatternVisible)
                    patronesCorte['Primer plano - Patrón'] = (
                        configuracion.SurfaceBackgroundPatternId)
                    patronesCorte['Primer plano - Color'] = (
                        color_consultar_rgb(
                            configuracion.SurfaceBackgroundPatternColor))
                    # Lo relativo al patron de fondo
                    patronesCorte['Fondo - Visibilidad'] = (
                        configuracion.IsCutBackgroundPatternVisible)
                    patronesCorte['Fondo - Patrón'] = (
                        configuracion.CutBackgroundPatternId)
                    patronesCorte['Fondo - Color'] = (
                        color_consultar_rgb(
                            configuracion.CutBackgroundPatternColor))
                    # Se almacena la informacion de las lineas de proyeccion
                    corte['Patrones'] = patronesCorte
                    # Se almacena toda la informacion relativa a corte
                    datos['Corte'] = corte

                    # Se consulta si esta a medio tono
                    datos['Tramado'] = configuracion.Halftone
                    salida[nombreFiltro] = datos
            else:
                salida = 'No hay filtros aplicados en la vista.'
        except:
           salida = 'No se puede aplicar \nfiltros a esta vista.'
    else:
        salida = ('Se esperaba una vista.\n'
                  'Revisar si es una plantilla de vista.')
    return salida


def seccion_paralela_por_curva(curva, desfase, altura):
    """
    Uso:
    Entrada:
        curva <curve>: Revit curve.
        desfase <float>: Separacion del muro. Siempre en unidades metricas.
        altura <float>: Altura del muro.
    Salida:
    """
    # Convierto unidades a internas
    o = unidades_modelo_a_internas_longitud(float(desfase))
    h = unidades_modelo_a_internas_longitud(float(altura))

    bbMax = XYZ(curva.GetEndPoint(1).X + desfase, curva.GetEndPoint(0).X - desfase, h + desfase)
    bbMin = XYZ(curva.GetEndPoint(1).X + desfase, curva.GetEndPoint(0).X - desfase, h + desfase)
    i = curva.GetEndPoint(0) # XYZ
    f = curva.GetEndPoint(1) # XYZ
    d = f - i # XYZ
    l = d.GetLength()

    # Definir los ejes
    x = d.Normalize()
    y = XYZ.BasisZ
    z = x.CrossProduct(y)

    # Crear una instancia de la clase Transform
    t = Transform.Identity
    t.Origin = i + 0.5*d
    t.BasisX = x
    t.BasisY = y
    t.BasisZ = z

    # Creamos BoundingBox
    caja = BoundingBoxXYZ()
    caja.Transform = t
    caja.Min = XYZ(- (0.5*l + o), i.Z - o, - o)
    caja.Max = XYZ(0.5*l + o, h + o, o)

    idTipoFamilia = id_tipo_familia_vista()['Section']

    TransactionManager.Instance.EnsureInTransaction(doc)
    seccion = ViewSection.CreateSection(doc, idTipoFamilia, caja)
    TransactionManager.Instance.TransactionTaskDone()

    return seccion


def seccion_perpendicular_por_curva(curva, desfase, altura):
    """
    Uso:
    Entrada:
        curva <curve>: Revit curve.
        desfase <float>: Separacion del muro. Siempre en unidades metricas.
        altura <float>: Altura del muro.
    Salida:
    """
    # Convierto unidades a internas
    o = unidades_modelo_a_internas_longitud(float(desfase))
    h = unidades_modelo_a_internas_longitud(float(altura))

    bbMax = XYZ(curva.GetEndPoint(1).X + desfase, curva.GetEndPoint(0).X - desfase, h + desfase)
    bbMin = XYZ(curva.GetEndPoint(1).X + desfase, curva.GetEndPoint(0).X - desfase, h + desfase)
    i = curva.GetEndPoint(0) # XYZ
    f = curva.GetEndPoint(1) # XYZ
    d = f - i # XYZ
    l = d.GetLength()

    # Definir los ejes
    z = d.Normalize()
    y = XYZ.BasisZ
    x = y.CrossProduct(z)

    # Crear una instancia de la clase Transform
    t = Transform.Identity
    t.Origin = i + 0.5*d
    t.BasisX = x
    t.BasisY = y
    t.BasisZ = z

    # Creamos BoundingBox
    caja = BoundingBoxXYZ()
    caja.Transform = t
    caja.Min = XYZ(- o, i.Z - o, - o)
    caja.Max = XYZ(o, h + o, o)

    idTipoFamilia = id_tipo_familia_vista()['Section']

    TransactionManager.Instance.EnsureInTransaction(doc)
    seccion = ViewSection.CreateSection(doc, idTipoFamilia, caja)
    TransactionManager.Instance.TransactionTaskDone()

    return seccion


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Conversion de unidades
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def unidades_internas_a_modelo_longitud(valor):
    """
    """
    if int(doc.Application.VersionNumber) >= 2022:
        unidadModelo = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()     
        return UnitUtils.ConvertFromInternalUnits(valor, unidadModelo)        
    else: 
        unidadModelo = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits     
        return UnitUtils.ConvertFromInternalUnits(valor, unidadModelo)


def unidades_internas_a_modelo_area(valor):
    """
    """
    if int(doc.Application.VersionNumber) >= 2022:
        unidadModelo = doc.GetUnits().GetFormatOptions(SpecTypeId.Area).GetUnitTypeId()     
        return UnitUtils.ConvertFromInternalUnits(valor, unidadModelo)        
    else: 
        unidadModelo = doc.GetUnits().GetFormatOptions(UnitType.UT_Area).DisplayUnits     
        return UnitUtils.ConvertFromInternalUnits(valor, unidadModelo)  


def unidades_modelo_a_internas_longitud(valor):
    """
    """
    if int(doc.Application.VersionNumber) >= 2022:
        unidadModelo = doc.GetUnits().GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()     
        return UnitUtils.ConvertToInternalUnits(valor, unidadModelo)        
    else: 
        unidadModelo = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits     
        return UnitUtils.ConvertToInternalUnits(valor, unidadModelo)

                                        
def cm_a_internas_longitud(valor):
    """
    """
    if int(doc.Application.VersionNumber) >= 2022:     
        return UnitUtils.ConvertToInternalUnits(valor, UnitType.Centimeters)
    else: 
        return UnitUtils.ConvertToInternalUnits(valor, DisplayUnitType.DUT_CENTIMETERS)
  

def convertir_XYZ_unidad_interna(punto): 
    """
    Uso: Crea un XYZ() en metros, y lo convierte a unidades internas.
    Cuidado: Dependencia de la funcion unidades_modelo_a_internas_longitud().
    """
    factor = unidades_modelo_a_internas_longitud(1)
    return punto.Multiply(factor)

