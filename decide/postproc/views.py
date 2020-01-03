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
            nv= nv+ out['votes'];

        perc = 0;
        
        if nv < ne:
            
            perc = ne/nv;
        
        else:
            
            perc = nv/ne;
    

        i = 0;

        while i < len(out):
            if ne > 0:
                seats_=0;
                seats_ = out[i]['votes']/perc

                out[i]['postproc'] = seats_;

                i= i+1;

                ne = ne - seats_ ;
            else:
                break;
        
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | SIMPLE
         * seats : int
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
        s = request.data.get('seats')

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t =='SIMPLE':
            return self.simple(opts, s)

        return Response({})
