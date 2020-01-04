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
            });

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
        
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | SIMPLE
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
        
        elif t =='SIMPLE':
            return self.simple(opts, s)

        return Response({})
