from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def paridad(self, options):
		out = [];

		    paridad = True;
		    for opt in options:

		        out.append({
		            **opt,
		            'paridad': [],
		        })
		        
		    for i in out:
		        escanos = i['postproc'];
		        candidatos = i['candidatos'];
		        hombres = []
		        mujeres = []
		        for cand in candidatos:
		            if cand['sexo'] == 'hombre':
		                hombres.append(cand)
		            elif cand['sexo'] == 'mujer':
		                mujeres.append(cand)
		        e=0;
		        while escanos > 0:
		            if paridad :
		                i['paridad'].append(mujeres[e])
		                paridad = False;
		            else:
		                i['paridad'].append(hombres[e])
		                paridad = True;
		                e = e+1;
		            escanos -= 1

        return Response(out)



    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'PARIDAD':
            return self.paridad(opts)

        return Response({})
