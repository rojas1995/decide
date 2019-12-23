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
        out = options;
        
        i= 0;

        paridad = True;
        for opt in options:

            out.append({
                **opt,
                'paridad': [],
            })
            
        while i < len(out):
        	escanos = out['postproc'];
        	candidatos = out['candidatos'];
        	hombres = filter(lambda hombre: candidatos['sexo'] == 'hombre', candidatos)
        	mujeres = filter(lambda mujer: candidatos['sexo'] == 'mujer', candidatos)
        	e=0;
        	while escanos > 0:
        		if paridad :
        			out['paridad'].append(mujeres[e])
        			paridad = False;
        		else:
        			out['paridad'].append(hombres[e])
        			paridad = True;
        			e = e+1;

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
