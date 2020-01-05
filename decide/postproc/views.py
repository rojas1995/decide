from rest_framework.views import APIView
from rest_framework.response import Response
import math


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)
    def simple(self, options, seats):

        out = []

        for opt in options:

            out.append({
                **opt,
                'postproc': 0,
            })

        out.sort(key=lambda x: -x['votes'])

        ne = seats;
        nv = 0;

        for votes in out:
            nv= nv+ votes['votes'];


        valor_escano = nv/ne;

        a = 0;        
        
        while ne > 0:
            
            if a < len(out):
                
                seats_ = math.trunc(out[a]['votes']/valor_escano)

                out[a]['postproc'] = seats_;

                ne = ne - seats_ ;
                
                a = a + 1
           
            else:

                actual = 0;

                i = 1;

                while i < len(out):

                    valorActual = out[actual]['votes']/valor_escano - out[actual]['postproc']

                    valorComparate = out[i]['votes']/valor_escano - out[i]['postproc']

                    if (valorActual >= valorComparate):

                        i = i + 1;

                    else:

                        actual = i;

                        i = i + 1;

                out[actual]['postproc'] = out[actual]['postproc'] + 1;

                ne = ne - 1;
        
        return out


    def dhondt(self, options, seats):

        out = []

        for opt in options:

            out.append({
                **opt,

                'postproc': 0,
            })

        out.sort(key=lambda x: -x['votes'])

        ne = seats;

        while ne > 0:

            actual = 0;

            i = 1;

            while i < len(out):

                valorActual = out[actual]['votes'] / (out[actual]['postproc'] + 1);

                valorComparate = out[i]['votes'] / (out[i]['postproc'] + 1);

                if (valorActual >= valorComparate):

                    i = i + 1;

                else:

                    actual = i;

                    i = i + 1;

            out[actual]['postproc'] = out[actual]['postproc'] + 1;

            ne = ne - 1;
            
        return out


    def paridad(self, options):
        out = []

        for opt in options:

            out.append({
                **opt,
                'paridad': [],
            })

                    
        for i in out:
            escanos = i['postproc']
            candidatos = i['candidatos']
            hombres = []
            mujeres = []
            for cand in candidatos:
                if cand['sexo'] == 'hombre':
                    hombres.append(cand)
                elif cand['sexo'] == 'mujer':
                    mujeres.append(cand)
                    
            h=0
            m=0
            
            paridad = True
            while escanos > 0:
                if paridad:
                    
                    if m < len(mujeres):
                        
                        i['paridad'].append(mujeres[m])
                        m = m + 1
                        
                    else:
                        
                        i['paridad'].append(hombres[h])
                        h = h + 1
                        
                    paridad = False
                    
                else:
                    
                    if h < len(hombres):
                        
                        i['paridad'].append(hombres[h])
                        h = h + 1
                        
                    else:
                        
                        i['paridad'].append(mujeres[m])
                        m = m + 1
                        
                    paridad = True
                    
                escanos -= 1
        return out


    def check_json(self, opts):
        out = []
        check = False
        for opt in opts:

            out.append({
                **opt
            })

        for i in out:
            candidatos = i['candidatos']
            hombres = []
            mujeres = []
            for cand in candidatos:
                if cand['sexo'] == 'hombre':
                    hombres.append(cand)
                elif cand['sexo'] == 'mujer':
                    mujeres.append(cand)
           
            check = self.porcentajes_mujeres_homnres(hombres, mujeres)
            if ~check:
                break
        return check

    def porcentajes_mujeres_homnres(self, hombres, mujeres):
        total = len(hombres)+len(mujeres)
        por_hombres = len(hombres)/total
        por_mujeres = len(mujeres)/total
        if (por_mujeres < 0.4) | (por_hombres < 0.4):
            return False
        else:
            return True

    def post(self, request):
        """
         * type: IDENTITY | DHONDTP | DHONDT | SIMPLE
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type')
        opts = request.data.get('options', [])
        s = request.data.get('seats')

        if t == 'IDENTITY':
            return self.identity(opts)
        
        elif t =='SIMPLE':
            return(self.simple(opts, s))
        
        elif t == 'SIMPLEP':
            check = self.check_json(opts)
            if check:
                options = []
                options = self.simple(opts, s)
                return response(self.paridad(opts))
            else:
                return Response({'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'})

        elif t == 'DHONDTP':
            check = self.check_json(opts)
            if check:
                options = []
                options = self.dhondt(opts, s)
                return response(self.paridad(options))
            else:
                return Response({'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'})
              
        elif t == 'DHONDT':
            return response(self.dhondt(opts, s))

        return Response({})
