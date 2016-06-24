from multiprocessing import Pool
import event_scrapp as es
from functools import partial

candidates=set(['Barack Obama','Hillary Clinton','Bill Richardson','John Edwards','Christopher Dodd','Joe Biden','John McCain','Mike Huckabee','Mitt Romney','Rudy Giuliani','Fred Thompson','Barack Obama','Mitt Romney','Ron Paul',
    'Newt Gingrich','Rick Santorum','Rick Perry','Jon Huntsman','Michele Bachmann','Herman Cain','Tim Pawlenty','Donald Trump','Hillary Clinton',
    'Bernie Sanders','Martin OMalley','Lincoln Chafee','Jim Webb','John Kasich','Ted Cruz','Marco Rubio','Ben Carson','Jeb Bush','Chris Christie',
    'Carly Fiorina','Rick Santorum','Rand Paul','Mike Huckabee','George Pataki','Lindsey Graham','Bobby Jindal','Scott Walker','Rick Perry'])

pool=Pool(24)

pool.map(partial(es.scrapp_candidate,path='event_registry/'),candidates)