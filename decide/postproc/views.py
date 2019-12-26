from rest_framework.views import APIView
from rest_framework.response import Response


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


    def dhondt(self, options, seats, paridad):

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
        
        if paridad:
            out = self.paridad(Response(out))
            return out
        else:
            return Response(out)


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
            e=0
            paridad = True
            while escanos > 0:
                if paridad:
                    i['paridad'].append(mujeres[e])
                    paridad = False
                else:
                    i['paridad'].append(hombres[e])
                    paridad = True
                    e = e+1
                escanos -= 1
        return Response(out)





    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * seats: int
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

        elif t == 'DHONDTP':
            return self.dhondt(opts, s, True)

        elif t == 'DHONDT':
            return self.dhondt(opts, s, False)

        return Response({})
