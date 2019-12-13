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
        elif t == 'DHONDT':
            return self.dhondt(opts, s)

        return Response({})
